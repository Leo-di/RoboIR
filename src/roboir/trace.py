from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from .graph import StepResult
from .scene import SceneGraph
from .embodied import TaskFrame


@dataclass
class TraceEvent:
    kind: str
    payload: Dict[str, Any]


@dataclass
class TraceLog:
    events: List[TraceEvent] = field(default_factory=list)

    def add(self, kind: str, **payload: Any) -> None:
        self.events.append(TraceEvent(kind=kind, payload=payload))

    def add_scene(self, scene_graph: SceneGraph) -> None:
        self.add("scene", summary=scene_graph.summary())

    def add_task_frame(self, task_frame: TaskFrame) -> None:
        self.add("frame", **task_frame.summary())

    def add_step(self, node_name: str, result: StepResult, phase: str | None = None) -> None:
        payload = {"node": node_name, "status": result.status.value, "message": result.message, "artifacts": result.artifacts}
        if phase is not None:
            payload["phase"] = phase
        self.add("step", **payload)

    def export_json(self, path: str | Path) -> None:
        path = Path(path)
        path.write_text(json.dumps([asdict(event) for event in self.events], ensure_ascii=False, indent=2), encoding="utf-8")
