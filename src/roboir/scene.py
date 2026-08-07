from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary(),
            "objects": [asdict(scene_object) for scene_object in self.objects.values()],
            "relations": [asdict(relation) for relation in self.relations],
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "SceneGraph":
        graph = cls()
        for item in payload.get("objects", []):
            graph.add_object(SceneObject(**item))
        for item in payload.get("relations", []):
            graph.add_relation(SpatialRelation(**item))
        return graph

    def save_json(self, path: str | Path) -> None:
        path = Path(path)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load_json(cls, path: str | Path) -> "SceneGraph":
        path = Path(path)
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))
