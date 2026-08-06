from pathlib import Path

from roboir import Affordance, AffordanceMap, GraphNode, GraphRuntime, GraphStatus, RoboIRRuntime, SceneGraph, SceneObject, SkillPlanner, SkillRegistry, SkillSpec, StepResult


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
