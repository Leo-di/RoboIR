from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional

from .affordance import Affordance
from .embodied import TaskFrame
from .scene import SceneGraph


@dataclass
class SkillContext:
    goal: str
    scene_graph: SceneGraph
    task_frame: TaskFrame | None = None
    state: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SkillSpec:
    name: str
    description: str
    requires: List[str] = field(default_factory=list)
    satisfies: List[str] = field(default_factory=list)
    precondition: Optional[Callable[[SkillContext], bool]] = None
    supported_phases: tuple[str, ...] = ()
    region_bias: tuple[str, ...] = ()
    contact_modes: tuple[str, ...] = ()

    def is_available(self, context: SkillContext) -> bool:
        if self.precondition is None:
            return True
        return self.precondition(context)

    def supports_task_frame(self, task_frame: TaskFrame | None) -> bool:
        if task_frame is None:
            return True
        if self.supported_phases and task_frame.phase.value not in self.supported_phases:
            return False
        if self.region_bias:
            region_names = {constraint.name for constraint in task_frame.region_constraints}
            if region_names.isdisjoint(self.region_bias):
                return False
        return True


@dataclass
class SkillRegistry:
    skills: Dict[str, SkillSpec] = field(default_factory=dict)

    def register(self, skill: SkillSpec) -> None:
        self.skills[skill.name] = skill

    def get(self, name: str) -> SkillSpec:
        return self.skills[name]

    def match_affordance(self, affordance: Affordance) -> List[SkillSpec]:
        return [
            skill
            for skill in self.skills.values()
            if affordance.action in skill.satisfies or affordance.name in skill.requires
        ]
