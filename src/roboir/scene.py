from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class SceneObject:
    object_id: str
    label: str
    category: str
    pose: tuple[float, float, float] | None = None
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SpatialRelation:
    subject_id: str
    predicate: str
    object_id: str
    confidence: float = 1.0


@dataclass
class SceneGraph:
    objects: Dict[str, SceneObject] = field(default_factory=dict)
    relations: List[SpatialRelation] = field(default_factory=list)

    def add_object(self, scene_object: SceneObject) -> None:
        self.objects[scene_object.object_id] = scene_object

    def add_relation(self, relation: SpatialRelation) -> None:
        self.relations.append(relation)

    def get(self, object_id: str) -> SceneObject:
        return self.objects[object_id]

    def find_by_category(self, category: str) -> List[SceneObject]:
        return [scene_object for scene_object in self.objects.values() if scene_object.category == category]

    def related_to(self, object_id: str, predicate: Optional[str] = None) -> List[SpatialRelation]:
        matches = [relation for relation in self.relations if relation.subject_id == object_id]
        if predicate is not None:
            matches = [relation for relation in matches if relation.predicate == predicate]
        return matches

    def summary(self) -> Dict[str, Any]:
        return {
            "object_count": len(self.objects),
            "relation_count": len(self.relations),
            "categories": sorted({scene_object.category for scene_object in self.objects.values()}),
        }
