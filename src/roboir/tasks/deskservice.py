from __future__ import annotations

from ..affordance import Affordance, AffordanceMap
from ..benchmark import TaskBenchmark, TaskCase
from ..embodied import RegionConstraint, TaskFrame, TaskPhase
from ..graph import GraphNode, GraphRuntime, GraphStatus, StepResult
from ..plugin import PluginManager, StaticPlugin
from ..recovery import RecoveryManager
from ..runtime import RoboIRRuntime
from ..scene import SceneGraph, SceneObject, SpatialRelation
from ..skill import SkillRegistry, SkillSpec
from .base import TaskPack


def _build_plan() -> list[GraphNode]:
    def scan(_context, memory):
        memory.store("desk_state", "scanned", source="scan_workspace")
        return StepResult(GraphStatus.SUCCESS, "workspace scanned")

    def fetch(_context, memory):
        memory.store("item_state", "fetched", source="fetch_part")
        return StepResult(GraphStatus.SUCCESS, "part fetched")

    def route(_context, memory):
        memory.store("route_state", "aligned", source="route_to_station")
        return StepResult(GraphStatus.SUCCESS, "route aligned")

    def place(_context, memory):
        memory.store("handoff_state", "placed", source="place_on_tray")
        return StepResult(GraphStatus.SUCCESS, "item placed")

    return [
        GraphNode(name="scan_workspace", skill_name="scan_workspace", phase=TaskPhase.OBSERVE, action=scan, region_hint="desktop"),
        GraphNode(name="fetch_part", skill_name="fetch_part", phase=TaskPhase.GROUND, action=fetch, region_hint="pickup_zone", contact_mode="pinch"),
        GraphNode(name="route_to_station", skill_name="route_to_station", phase=TaskPhase.PLAN, action=route, region_hint="transfer_lane"),
        GraphNode(name="place_on_tray", skill_name="place_on_tray", phase=TaskPhase.EXECUTE, action=place, region_hint="tray_zone", contact_mode="setdown"),
    ]


def _build_scene() -> SceneGraph:
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="desk_1", label="assembly desk", category="desk"))
    scene.add_object(SceneObject(object_id="part_1", label="part bin", category="item"))
    scene.add_object(SceneObject(object_id="tray_1", label="output tray", category="tray"))
    scene.add_object(SceneObject(object_id="station_1", label="inspection station", category="station"))
    scene.add_relation(SpatialRelation(subject_id="part_1", predicate="near", object_id="desk_1", confidence=0.8))
    return scene


def _build_benchmark(scene_graph: SceneGraph, plan: list[GraphNode]) -> TaskBenchmark:
    benchmark = TaskBenchmark()
    benchmark.add(TaskCase(name="deskservice_kitting", goal="desk assembly handoff", scene_graph=scene_graph, plan=plan))
    benchmark.add(TaskCase(name="deskservice_routing", goal="desk assembly handoff", scene_graph=scene_graph, plan=plan))
    return benchmark


def build_deskservice_pack() -> TaskPack:
    registry = SkillRegistry()
    affordance_map = AffordanceMap()
    plugin_manager = PluginManager()
    plugin_manager.add(
        StaticPlugin(
            name="deskservice_core",
            skills=(
                SkillSpec(name="scan_workspace", description="Scan the work surface", satisfies=["inspect"], supported_phases=(TaskPhase.OBSERVE.value,)),
                SkillSpec(name="fetch_part", description="Fetch a part", satisfies=["pick"], supported_phases=(TaskPhase.GROUND.value,), region_bias=("pickup_zone",), contact_modes=("pinch",)),
                SkillSpec(name="route_to_station", description="Route an object to station", satisfies=["move"], supported_phases=(TaskPhase.PLAN.value,), region_bias=("transfer_lane",)),
                SkillSpec(name="place_on_tray", description="Place an item on tray", satisfies=["place"], supported_phases=(TaskPhase.EXECUTE.value,), region_bias=("tray_zone",), contact_modes=("setdown",)),
            ),
            affordances=(
                Affordance(name="desk_surface", target_category="desk", action="inspect", region_hint="desktop"),
                Affordance(name="part_grasp", target_category="item", action="pick", region_hint="pickup_zone", contact_mode="pinch"),
                Affordance(name="station_route", target_category="station", action="move", region_hint="transfer_lane"),
                Affordance(name="tray_surface", target_category="tray", action="place", region_hint="tray_zone", contact_mode="setdown"),
            ),
        )
    )
    plugin_manager.install(registry, affordance_map)
    runtime = RoboIRRuntime(graph_runtime=GraphRuntime(skill_registry=registry, affordance_map=affordance_map), recovery_manager=RecoveryManager())
    scene_graph = _build_scene()
    plan = _build_plan()
    benchmark = _build_benchmark(scene_graph, plan)
    return TaskPack(name="deskservice", runtime=runtime, scene_graph=scene_graph, plan=plan, benchmark=benchmark)
