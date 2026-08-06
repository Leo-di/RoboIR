from pathlib import Path

from roboir import Affordance, AffordanceMap, GraphNode, GraphRuntime, GraphStatus, HumanInTheLoopManager, InterventionRequest, Pose6D, RoboIRRuntime, SceneGraph, SceneObject, SkillPlanner, SkillRegistry, SkillSpec, StepResult, SpatialMemory, TraceAnalyzer, TraceLog
from roboir.analysis import TraceSummary
from roboir.benchmark import TaskBenchmark, TaskCase
from roboir.dataset import TraceDataset
from roboir.failure import FailureCategory, FailureClassifier, FailureLog
from roboir.policy import RuleBasedPolicy
from roboir.report import ExecutionReport
from roboir.suite import TaskSuite
from roboir.tasks import build_task_pack, default_task_catalog
from roboir.visualization import trace_to_mermaid


def make_runtime() -> RoboIRRuntime:
    registry = SkillRegistry()
    registry.register(SkillSpec(name="pick", description="pick", satisfies=["pick"]))
    affordance_map = AffordanceMap([Affordance(name="grasp", target_category="item", action="pick")])
    return RoboIRRuntime(graph_runtime=GraphRuntime(skill_registry=registry, affordance_map=affordance_map))


def test_scene_graph_summary():
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="obj_1", label="cup", category="item"))
    assert scene.summary()["object_count"] == 1
    assert scene.find_by_category("item")[0].label == "cup"


def test_affordance_query():
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="obj_1", label="cup", category="item"))
    runtime = make_runtime()
    matches = runtime.affordance_map.query(scene)
    assert len(matches) == 1
    assert matches[0][1].action == "pick"


def test_skill_planner_ranks_candidates():
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="obj_1", label="cup", category="item"))
    runtime = make_runtime()
    planner = SkillPlanner(runtime.graph_runtime.skill_registry)
    best = planner.best(scene, list(runtime.affordance_map.affordances))
    assert best is not None
    assert best.skill.name == "pick"


def test_runtime_run_report_and_failure_log():
    runtime = make_runtime()
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="obj_1", label="cup", category="item"))

    def action(_context, memory):
        return StepResult(GraphStatus.FAILED, "pick failed", artifacts={"failure_category": "affordance"})

    report = runtime.run_report("pick cup", scene, [GraphNode(name="pick_step", skill_name="pick", action=action)])
    assert report.failure_count == 1
    assert report.failure_log is not None
    assert report.failure_log.summary()[FailureCategory.AFFORDANCE.value] == 1
    assert runtime.last_report is report


def test_runtime_records_trace_and_memory(tmp_path: Path):
    runtime = make_runtime()
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="obj_1", label="cup", category="item"))

    def action(_context, memory):
        memory.store("step", "done", source="pick")
        return StepResult(GraphStatus.SUCCESS, "picked")

    results = runtime.run("pick cup", scene, [GraphNode(name="pick_step", skill_name="pick", action=action)])
    assert results[0].status is GraphStatus.SUCCESS
    assert runtime.graph_runtime.memory.get("pick_step") == "picked"
    assert len(runtime.trace_log.events) == 2
    trace_path = tmp_path / "trace.json"
    runtime.trace_log.export_json(trace_path)
    assert trace_path.exists()


def test_runtime_recovery_policy_applies():
    runtime = make_runtime()
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="obj_1", label="cup", category="item"))

    def action(_context, memory):
        return StepResult(GraphStatus.FAILED, "grasp failed")

    def recover(_context, memory, _result):
        memory.store("recover_called", True, source="policy")
        return StepResult(GraphStatus.RECOVERED, "retry succeeded")

    runtime.recovery_manager.add(recover)
    results = runtime.run("pick cup", scene, [GraphNode(name="pick_step", skill_name="pick", action=action)])
    assert results[0].status is GraphStatus.RECOVERED
    assert runtime.graph_runtime.memory.get("recover_called") is True


def test_trace_dataset_roundtrip(tmp_path: Path):
    runtime = make_runtime()
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="obj_1", label="cup", category="item"))

    def action(_context, memory):
        return StepResult(GraphStatus.SUCCESS, "picked")

    runtime.run("pick cup", scene, [GraphNode(name="pick_step", skill_name="pick", action=action)])
    dataset = TraceDataset.from_trace_log("pick cup", scene, runtime.trace_log, runtime.graph_runtime.memory.snapshot())
    path = tmp_path / "dataset.jsonl"
    dataset.save_jsonl(path)
    loaded = TraceDataset.load_jsonl(path)
    assert loaded.examples[0].goal == "pick cup"


def test_policy_decision():
    runtime = make_runtime()
    planner = SkillPlanner(runtime.graph_runtime.skill_registry)
    policy = RuleBasedPolicy(planner)
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="obj_1", label="cup", category="item"))
    decision = policy.decide(scene, runtime.affordance_map)
    assert decision.candidate is not None


def test_workcell_pack_and_benchmark():
    pack = build_task_pack("workcell")
    report = pack.benchmark.run(pack.runtime)
    assert report.score >= 0.0
    assert len(report.outcomes) == 2


def test_task_suite_runs_multiple_packs():
    suite = TaskSuite(["workcell", "lab", "office", "retail"])
    report = suite.run()
    assert len(report.outcomes) == 4
    assert report.summary()["suite_size"] == 4.0


def test_task_catalog_and_spatial_intervention_and_mermaid(tmp_path: Path):
    catalog = default_task_catalog()
    assert catalog.describe("workcell").domain == "industrial-service"

    spatial = SpatialMemory()
    spatial.update("obj_1", (1, 2, 3, 0, 0, 0), source="sensor")
    assert spatial.get("obj_1") == (1, 2, 3, 0, 0, 0)

    manager = HumanInTheLoopManager(handler=lambda request: StepResult(GraphStatus.RECOVERED, f"helped {request.node_name}"))
    request = InterventionRequest(
        goal="pick cup",
        node_name="step_1",
        reason="need help",
        scene_summary={"object_count": 1},
        memory_snapshot={},
        spatial_snapshot=spatial.snapshot(),
        last_result=StepResult(GraphStatus.FAILED, "bad grasp"),
    )
    response = manager.request(request)
    assert response is not None
    assert response.status is GraphStatus.RECOVERED

    runtime = make_runtime()
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="obj_1", label="cup", category="item"))

    def action(_context, memory):
        return StepResult(GraphStatus.SUCCESS, "picked")

    runtime.run("pick cup", scene, [GraphNode(name="pick_step", skill_name="pick", action=action)])
    mermaid = trace_to_mermaid(runtime.trace_log)
    assert "flowchart TD" in mermaid


def test_execution_report_and_classifier():
    summary = TraceSummary(task_count=1, event_count=2, step_count=1, status_counts={"success": 1}, goal_counts={"pick": 1}, memory_key_counts={"pick_step": 1})
    failure_log = FailureLog()
    report = ExecutionReport(goal="pick cup", results=[StepResult(GraphStatus.SUCCESS, "picked")], trace_summary=summary, failure_log=failure_log)
    assert report.success_count == 1
    assert report.summary()["goal"] == "pick cup"

    classifier = FailureClassifier()
    category = classifier.classify(StepResult(GraphStatus.FAILED, "grasp failed", artifacts={"failure_category": "affordance"}))
    assert category is FailureCategory.AFFORDANCE
