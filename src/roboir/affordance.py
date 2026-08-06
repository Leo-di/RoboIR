from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional

from .scene import SceneGraph, SceneObject


@dataclass(frozen=True)
class Affordance:
    name: str
    target_category: str
    action: str
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AffordanceMap:
    affordances: List[Affordance] = field(default_factory=list)

    def register(self, affordance: Affordance) -> None:
        self.affordances.append(affordance)

    def for_object(self, scene_object: SceneObject) -> List[Affordance]:
        return [
            affordance
            for affordance in self.affordances
            if affordance.target_category == scene_object.category
        ]

    def query(self, scene_graph: SceneGraph, predicate: Optional[Callable[[Affordance], bool]] = None) -> List[tuple[SceneObject, Affordance]]:
        matches: List[tuple[SceneObject, Affordance]] = []
        for scene_object in scene_graph.objects.values():
            for affordance in self.for_object(scene_object):
                if predicate is None or predicate(affordance):
                    matches.append((scene_object, affordance))
        return matches
