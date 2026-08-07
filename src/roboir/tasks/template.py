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
        memory.store("template_state", "inspected", source="template_inspect")
        return StepResult(GraphStatus.SUCCESS, "template inspected")

    return [
        GraphNode(name="template_inspect", skill_name="template_inspect", action=inspect),
    ]


def _build_scene() -> SceneGraph:
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="item_1", label="example item", category="item"))
    return scene


def _build_benchmark(scene_graph: SceneGraph, plan: list[GraphNode]) -> TaskBenchmark:
    benchmark = TaskBenchmark()
    benchmark.add(TaskCase(name="template_case", goal="template goal", scene_graph=scene_graph, plan=plan))
    return benchmark


def build_task_pack_template(name: str = "your_pack_name") -> TaskPack:
    registry = SkillRegistry()
    affordance_map = AffordanceMap()
    plugin_manager = PluginManager()
    plugin_manager.add(
        StaticPlugin(
            name="template_core",
            skills=(
                SkillSpec(name="template_inspect", description="Inspect a template object", satisfies=["inspect"]),
            ),
            affordances=(
                Affordance(name="template_surface", target_category="item", action="inspect"),
            ),
        )
    )
    plugin_manager.install(registry, affordance_map)
    runtime = RoboIRRuntime(graph_runtime=GraphRuntime(skill_registry=registry, affordance_map=affordance_map), recovery_manager=RecoveryManager())
    scene_graph = _build_scene()
    plan = _build_plan()
    benchmark = _build_benchmark(scene_graph, plan)
    return TaskPack(name=name, runtime=runtime, scene_graph=scene_graph, plan=plan, benchmark=benchmark)
