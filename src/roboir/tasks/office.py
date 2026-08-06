from __future__ import annotations

from ..affordance import Affordance, AffordanceMap
from ..benchmark import TaskBenchmark, TaskCase
from ..graph import GraphNode, GraphRuntime, GraphStatus, StepResult
from ..plugin import PluginManager, StaticPlugin
from ..recovery import RecoveryManager
from ..runtime import RoboIRRuntime
from ..scene import SceneGraph, SceneObject
from ..skill import SkillRegistry, SkillSpec
from .base import TaskPack


def _build_plan() -> list[GraphNode]:
    def inspect(_context, memory):
        memory.store("desk_state", "inspected", source="inspect_desk")
        return StepResult(GraphStatus.SUCCESS, "desk inspected")

    def fetch(_context, memory):
        memory.store("item_state", "fetched", source="fetch_item")
        return StepResult(GraphStatus.SUCCESS, "item fetched")

    def deliver(_context, memory):
        memory.store("item_state", "delivered", source="deliver_item")
        return StepResult(GraphStatus.SUCCESS, "item delivered")

    return [
        GraphNode(name="inspect_desk", skill_name="inspect_desk", action=inspect),
        GraphNode(name="fetch_item", skill_name="fetch_item", action=fetch),
        GraphNode(name="deliver_item", skill_name="deliver_item", action=deliver),
    ]


def _build_scene() -> SceneGraph:
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="desk_1", label="desk", category="desk"))
    scene.add_object(SceneObject(object_id="item_1", label="folder", category="item"))
    scene.add_object(SceneObject(object_id="handoff_1", label="handoff zone", category="zone"))
    return scene


def _build_benchmark(scene_graph: SceneGraph, plan: list[GraphNode]) -> TaskBenchmark:
    benchmark = TaskBenchmark()
    benchmark.add(TaskCase(name="office_fetch", goal="office logistics", scene_graph=scene_graph, plan=plan))
    benchmark.add(TaskCase(name="office_handoff", goal="office logistics", scene_graph=scene_graph, plan=plan))
    return benchmark


def build_office_pack() -> TaskPack:
    registry = SkillRegistry()
    affordance_map = AffordanceMap()
    plugin_manager = PluginManager()
    plugin_manager.add(
        StaticPlugin(
            name="office_core",
            skills=(
                SkillSpec(name="inspect_desk", description="Inspect a desk", satisfies=["inspect"]),
                SkillSpec(name="fetch_item", description="Fetch an item", satisfies=["pick"]),
                SkillSpec(name="deliver_item", description="Deliver an item", satisfies=["place"]),
            ),
            affordances=(
                Affordance(name="desk_surface", target_category="desk", action="inspect"),
                Affordance(name="item_grasp", target_category="item", action="pick"),
                Affordance(name="handoff_zone", target_category="zone", action="place"),
            ),
        )
    )
    plugin_manager.install(registry, affordance_map)
    runtime = RoboIRRuntime(graph_runtime=GraphRuntime(skill_registry=registry, affordance_map=affordance_map), recovery_manager=RecoveryManager())
    scene_graph = _build_scene()
    plan = _build_plan()
    benchmark = _build_benchmark(scene_graph, plan)
    return TaskPack(name="office", runtime=runtime, scene_graph=scene_graph, plan=plan, benchmark=benchmark)
