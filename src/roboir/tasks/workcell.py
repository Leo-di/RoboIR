from __future__ import annotations

from ..affordance import AffordanceMap
from ..benchmark import TaskBenchmark, TaskCase
from ..graph import GraphNode, GraphRuntime, GraphStatus, StepResult
from ..plugins import default_workcell_plugins
from ..recovery import RecoveryManager
from ..runtime import RoboIRRuntime
from ..scene import SceneGraph, SceneObject
from ..skill import SkillRegistry
from .base import TaskPack


def _build_plan() -> list[GraphNode]:
    def inspect(_context, memory):
        memory.store("box_state", "opened", source="detect_object")
        return StepResult(GraphStatus.SUCCESS, "box detected")

    def pick(_context, memory):
        memory.store("item_state", "picked", source="grasp_object")
        return StepResult(GraphStatus.SUCCESS, "item picked")

    def place(_context, memory):
        memory.store("tray_state", "loaded", source="place_object")
        return StepResult(GraphStatus.SUCCESS, "item placed")

    return [
        GraphNode(name="inspect_box", skill_name="detect_object", action=inspect),
        GraphNode(name="pick_item", skill_name="grasp_object", action=pick),
        GraphNode(name="place_item", skill_name="place_object", action=place),
    ]


def _build_scene() -> SceneGraph:
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="box_1", label="kit box", category="box"))
    scene.add_object(SceneObject(object_id="item_1", label="screwdriver", category="item"))
    scene.add_object(SceneObject(object_id="tray_1", label="tray", category="tray"))
    return scene


def _build_benchmark(scene_graph: SceneGraph, plan: list[GraphNode]) -> TaskBenchmark:
    benchmark = TaskBenchmark()
    benchmark.add(TaskCase(name="kitting_success", goal="kitting", scene_graph=scene_graph, plan=plan))
    benchmark.add(TaskCase(name="kitting_recovery", goal="kitting", scene_graph=scene_graph, plan=plan))
    return benchmark


def build_workcell_pack() -> TaskPack:
    registry = SkillRegistry()
    affordance_map = AffordanceMap()
    default_workcell_plugins().install(registry, affordance_map)
    runtime = RoboIRRuntime(graph_runtime=GraphRuntime(skill_registry=registry, affordance_map=affordance_map), recovery_manager=RecoveryManager())
    scene_graph = _build_scene()
    plan = _build_plan()
    benchmark = _build_benchmark(scene_graph, plan)
    return TaskPack(name="workcell", runtime=runtime, scene_graph=scene_graph, plan=plan, benchmark=benchmark)
