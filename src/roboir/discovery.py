from __future__ import annotations

from importlib import import_module, metadata
from typing import Iterable, List

from .affordance import AffordanceMap
from .plugin import Plugin, PluginManager
from .skill import SkillRegistry


def load_plugin_from_module(module_name: str) -> Plugin | None:
    module = import_module(module_name)
    if hasattr(module, "PLUGIN"):
        plugin = getattr(module, "PLUGIN")
        if hasattr(plugin, "register") and hasattr(plugin, "name"):
            return plugin
    if hasattr(module, "build_plugin"):
        plugin = module.build_plugin()
        if hasattr(plugin, "register") and hasattr(plugin, "name"):
            return plugin
    return None


def discover_entry_point_plugins(group: str = "roboir.plugins") -> List[Plugin]:
    discovered: List[Plugin] = []
    try:
        entry_points = metadata.entry_points(group=group)
    except TypeError:
        entry_points = metadata.entry_points().select(group=group)
    for entry_point in entry_points:
        plugin = entry_point.load()
        if hasattr(plugin, "register") and hasattr(plugin, "name"):
            discovered.append(plugin)
    if not discovered:
        fallback = load_plugin_from_module("roboir_plugins.deskservice")
        if fallback is not None:
            discovered.append(fallback)
    return discovered


def load_plugin_manager_from_modules(module_names: Iterable[str]) -> PluginManager:
    manager = PluginManager()
    for module_name in module_names:
        plugin = load_plugin_from_module(module_name)
        if plugin is not None:
            manager.add(plugin)
    return manager


def install_plugins(manager: PluginManager, registry: SkillRegistry, affordance_map: AffordanceMap) -> None:
    manager.install(registry, affordance_map)
