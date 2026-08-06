from __future__ import annotations

from .affordance import Affordance
from .plugin import PluginManager, StaticPlugin
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
