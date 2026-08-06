from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .affordance import Affordance
from .embodied import GroundingDecision, TaskFrame
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

    def rank(self, scene_graph: SceneGraph, affordances: List[Affordance], task_frame: TaskFrame | None = None) -> List[SkillCandidate]:
        candidates: List[SkillCandidate] = []
        for scene_object in scene_graph.objects.values():
            for affordance in affordances:
                if affordance.target_category != scene_object.category:
                    continue
                for skill in self.registry.match_affordance(affordance):
                    if task_frame is not None:
                        if task_frame.target_object_ids and scene_object.object_id not in task_frame.target_object_ids:
                            continue
                        if not skill.supports_task_frame(task_frame):
                            continue
                    score = affordance.confidence
                    if skill.precondition is not None:
                        score += 0.1
                    if affordance.region_hint and affordance.region_hint in skill.region_bias:
                        score += 0.15
                    if affordance.contact_mode and affordance.contact_mode in skill.contact_modes:
                        score += 0.15
                    if affordance.preconditions:
                        score += min(len(affordance.preconditions), 3) * 0.05
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

    def best(self, scene_graph: SceneGraph, affordances: List[Affordance], task_frame: TaskFrame | None = None) -> Optional[SkillCandidate]:
        ranked = self.rank(scene_graph, affordances, task_frame=task_frame)
        return ranked[0] if ranked else None

    def decide(self, scene_graph: SceneGraph, affordances: List[Affordance], task_frame: TaskFrame | None = None) -> GroundingDecision | None:
        candidate = self.best(scene_graph, affordances, task_frame=task_frame)
        if candidate is None:
            return None
        reasons = [f"category={candidate.scene_object.category}", f"action={candidate.affordance.action}"]
        if candidate.affordance.region_hint:
            reasons.append(f"region={candidate.affordance.region_hint}")
        if candidate.affordance.contact_mode:
            reasons.append(f"contact={candidate.affordance.contact_mode}")
        return GroundingDecision(
            object_id=candidate.scene_object.object_id,
            affordance_name=candidate.affordance.name,
            skill_name=candidate.skill.name,
            score=candidate.score,
            reasons=tuple(reasons),
        )
