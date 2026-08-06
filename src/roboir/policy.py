from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .affordance import AffordanceMap
from .planner import SkillCandidate, SkillPlanner
from .scene import SceneGraph


@dataclass(frozen=True)
class PolicyDecision:
    candidate: Optional[SkillCandidate]
    reason: str


@dataclass
class RuleBasedPolicy:
    planner: SkillPlanner

    def decide(self, scene_graph: SceneGraph, affordance_map: AffordanceMap) -> PolicyDecision:
        if not self.planner.registry.skills:
            return PolicyDecision(candidate=None, reason="no registered skills")
        candidate = self.planner.best(scene_graph, list(affordance_map.affordances))
        if candidate is None:
            return PolicyDecision(candidate=None, reason="no candidate")
        return PolicyDecision(candidate=candidate, reason=f"selected {candidate.skill.name} for {candidate.scene_object.object_id}")
