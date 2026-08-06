from __future__ import annotations

from ..affordance import Affordance, AffordanceMap
from ..benchmark import TaskBenchmark, TaskCase
from ..graph import GraphNode, GraphRuntime, GraphStatus, StepResult
from ..plugin import PluginManager, StaticPlugin
from ..recovery import RecoveryManager
from ..runtime import RoboIRRuntime
from ..scene import SceneGraph, SceneObject, SpatialRelation
from ..skill import SkillRegistry, SkillSpec
from .base import TaskPack


def _build_plan() -> list[GraphNode]:
    def locate(_context, memory):
        memory.store("sample_state", "located", source="locate_sample")
        return StepResult(GraphStatus.SUCCESS, "sample located")

    def sort(_context, memory):
        memory.store("sample_state", "sorted", source="sort_sample")
        return StepResult(GraphStatus.SUCCESS, "sample sorted")

    def store(_context, memory):
        memory.store("sample_state", "stored", source="store_sample")
        return StepResult(GraphStatus.SUCCESS, "sample stored")

    return [
        GraphNode(name="locate_sample", skill_name="locate_sample", action=locate),
        GraphNode(name="sort_sample", skill_name="sort_sample", action=sort),
        GraphNode(name="store_sample", skill_name="store_sample", action=store),
    ]


def _build_scene() -> SceneGraph:
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="sample_1", label="vial", category="sample"))
    scene.add_object(SceneObject(object_id="rack_1", label="rack", category="rack"))
    scene.add_object(SceneObject(object_id="bin_1", label="waste bin", category="bin"))
    scene.add_relation(SpatialRelation(subject_id="sample_1", predicate="near", object_id="rack_1", confidence=0.7))
    return scene


def _build_benchmark(scene_graph: SceneGraph, plan: list[GraphNode]) -> TaskBenchmark:
    benchmark = TaskBenchmark()
    benchmark.add(TaskCase(name="lab_sorting", goal="sample handling", scene_graph=scene_graph, plan=plan))
    benchmark.add(TaskCase(name="lab_storage", goal="sample handling", scene_graph=scene_graph, plan=plan))
    return benchmark


def build_lab_pack() -> TaskPack:
    registry = SkillRegistry()
    affordance_map = AffordanceMap()
    plugin_manager = PluginManager()
    plugin_manager.add(
        StaticPlugin(
            name="lab_core",
            skills=(
                SkillSpec(name="locate_sample", description="Locate a sample", satisfies=["inspect"]),
                SkillSpec(name="sort_sample", description="Sort a sample", satisfies=["pick"]),
                SkillSpec(name="store_sample", description="Store a sample", satisfies=["place"]),
            ),
            affordances=(
                Affordance(name="rack_surface", target_category="rack", action="inspect"),
                Affordance(name="sample_grasp", target_category="sample", action="pick"),
                Affordance(name="bin_slot", target_category="bin", action="place"),
            ),
        )
    )
    plugin_manager.install(registry, affordance_map)
    runtime = RoboIRRuntime(graph_runtime=GraphRuntime(skill_registry=registry, affordance_map=affordance_map), recovery_manager=RecoveryManager())
    scene_graph = _build_scene()
    plan = _build_plan()
    benchmark = _build_benchmark(scene_graph, plan)
    return TaskPack(name="lab", runtime=runtime, scene_graph=scene_graph, plan=plan, benchmark=benchmark)
