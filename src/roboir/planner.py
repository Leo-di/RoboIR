from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .affordance import Affordance
from .scene import SceneGraph, SceneObject
from .skill import SkillRegistry, SkillSpec


@dataclass(frozen=True)
class SkillCandidate:
    scene_object: SceneObject
    affordance: Affordance
    skill: SkillSpec
    score: float


@dataclass
class SkillPlanner:
    registry: SkillRegistry

    def rank(self, scene_graph: SceneGraph, affordances: List[Affordance]) -> List[SkillCandidate]:
        candidates: List[SkillCandidate] = []
        for scene_object in scene_graph.objects.values():
            for affordance in affordances:
                if affordance.target_category != scene_object.category:
                    continue
                for skill in self.registry.match_affordance(affordance):
                    score = affordance.confidence
                    if skill.precondition is not None:
                        score += 0.1
                    candidates.append(
                        SkillCandidate(
                            scene_object=scene_object,
                            affordance=affordance,
                            skill=skill,
                            score=score,
                        )
                    )
        candidates.sort(key=lambda candidate: candidate.score, reverse=True)
        return candidates

    def best(self, scene_graph: SceneGraph, affordances: List[Affordance]) -> Optional[SkillCandidate]:
        ranked = self.rank(scene_graph, affordances)
        return ranked[0] if ranked else None
