from __future__ import annotations

from .affordance import Affordance
from .plugin import PluginManager, StaticPlugin
from .embodied import TaskPhase
from .skill import SkillSpec


def default_workcell_plugins() -> PluginManager:
    manager = PluginManager()
    manager.add(
        StaticPlugin(
            name="workcell_core",
            skills=(
                SkillSpec(name="detect_object", description="Locate an object", satisfies=["inspect"]),
                SkillSpec(name="grasp_object", description="Grasp an object", satisfies=["pick"]),
                SkillSpec(name="place_object", description="Place an object", satisfies=["place"]),
            ),
            affordances=(
                Affordance(name="top_surface", target_category="box", action="inspect"),
                Affordance(name="grasp_handle", target_category="item", action="pick"),
                Affordance(name="tray_zone", target_category="tray", action="place"),
            ),
        )
    )
    return manager


def default_deskservice_plugins() -> PluginManager:
    manager = PluginManager()
    manager.add(
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
    return manager
