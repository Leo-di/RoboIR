from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .affordance import Affordance, AffordanceMap
from .skill import SkillRegistry, SkillSpec


class Plugin(Protocol):
    name: str

    def register(self, registry: SkillRegistry, affordance_map: AffordanceMap) -> None:
        ...


@dataclass
class PluginManager:
    plugins: dict[str, Plugin] = field(default_factory=dict)

    def add(self, plugin: Plugin) -> None:
        self.plugins[plugin.name] = plugin

    def install(self, registry: SkillRegistry, affordance_map: AffordanceMap) -> None:
        for plugin in self.plugins.values():
            plugin.register(registry, affordance_map)


@dataclass(frozen=True)
class StaticPlugin:
    name: str
    skills: tuple[SkillSpec, ...] = ()
    affordances: tuple[Affordance, ...] = ()

    def register(self, registry: SkillRegistry, affordance_map: AffordanceMap) -> None:
        for skill in self.skills:
            registry.register(skill)
        for affordance in self.affordances:
            affordance_map.register(affordance)
