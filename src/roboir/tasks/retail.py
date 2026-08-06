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
    def scan(_context, memory):
        memory.store("cart_state", "scanned", source="scan_shelf")
        return StepResult(GraphStatus.SUCCESS, "shelf scanned")

    def restock(_context, memory):
        memory.store("item_state", "restocked", source="restock_item")
        return StepResult(GraphStatus.SUCCESS, "item restocked")

    def handoff(_context, memory):
        memory.store("handoff_state", "done", source="handoff_item")
        return StepResult(GraphStatus.SUCCESS, "handoff complete")

    return [
        GraphNode(name="scan_shelf", skill_name="scan_shelf", action=scan),
        GraphNode(name="restock_item", skill_name="restock_item", action=restock),
        GraphNode(name="handoff_item", skill_name="handoff_item", action=handoff),
    ]


def _build_scene() -> SceneGraph:
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="shelf_1", label="shelf", category="shelf"))
    scene.add_object(SceneObject(object_id="item_1", label="box cereal", category="item"))
    scene.add_object(SceneObject(object_id="cart_1", label="cart", category="cart"))
    return scene


def _build_benchmark(scene_graph: SceneGraph, plan: list[GraphNode]) -> TaskBenchmark:
    benchmark = TaskBenchmark()
    benchmark.add(TaskCase(name="retail_restock", goal="retail logistics", scene_graph=scene_graph, plan=plan))
    benchmark.add(TaskCase(name="retail_handoff", goal="retail logistics", scene_graph=scene_graph, plan=plan))
    return benchmark


def build_retail_pack() -> TaskPack:
    registry = SkillRegistry()
    affordance_map = AffordanceMap()
    plugin_manager = PluginManager()
    plugin_manager.add(
        StaticPlugin(
            name="retail_core",
            skills=(
                SkillSpec(name="scan_shelf", description="Scan a shelf", satisfies=["inspect"]),
                SkillSpec(name="restock_item", description="Restock an item", satisfies=["place"]),
                SkillSpec(name="handoff_item", description="Handoff an item", satisfies=["pick"]),
            ),
            affordances=(
                Affordance(name="shelf_face", target_category="shelf", action="inspect"),
                Affordance(name="cart_hold", target_category="cart", action="place"),
                Affordance(name="item_grip", target_category="item", action="pick"),
            ),
        )
    )
    plugin_manager.install(registry, affordance_map)
    runtime = RoboIRRuntime(graph_runtime=GraphRuntime(skill_registry=registry, affordance_map=affordance_map), recovery_manager=RecoveryManager())
    scene_graph = _build_scene()
    plan = _build_plan()
    benchmark = _build_benchmark(scene_graph, plan)
    return TaskPack(name="retail", runtime=runtime, scene_graph=scene_graph, plan=plan, benchmark=benchmark)
