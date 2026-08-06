from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


Pose6D = Tuple[float, float, float, float, float, float]


@dataclass(frozen=True)
class SpatialRecord:
    object_id: str
    pose: Pose6D
    source: str
    timestamp: float | None = None


@dataclass
class SpatialMemory:
    poses: Dict[str, Pose6D] = field(default_factory=dict)
    history: List[SpatialRecord] = field(default_factory=list)

    def update(self, object_id: str, pose: Pose6D, source: str = "sensor", timestamp: float | None = None) -> None:
        self.poses[object_id] = pose
        self.history.append(SpatialRecord(object_id=object_id, pose=pose, source=source, timestamp=timestamp))

    def get(self, object_id: str) -> Optional[Pose6D]:
        return self.poses.get(object_id)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "poses": {object_id: list(pose) for object_id, pose in self.poses.items()},
            "history": [
                {
                    "object_id": record.object_id,
                    "pose": list(record.pose),
                    "source": record.source,
                    "timestamp": record.timestamp,
                }
                for record in self.history
            ],
        }
