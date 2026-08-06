from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .graph import StepResult


@dataclass(frozen=True)
class InterventionRequest:
    goal: str
    node_name: str
    reason: str
    scene_summary: Dict[str, Any]
    memory_snapshot: Dict[str, Any]
    spatial_snapshot: Dict[str, Any]
    last_result: StepResult


InterventionHandler = Callable[[InterventionRequest], StepResult | None]


@dataclass(frozen=True)
class InterventionRecord:
    request: InterventionRequest
    response: StepResult | None = None


@dataclass
class InterventionLog:
    records: List[InterventionRecord] = field(default_factory=list)

    def add(self, request: InterventionRequest, response: StepResult | None = None) -> None:
        self.records.append(InterventionRecord(request=request, response=response))

    def export_json(self, path: str | Path) -> None:
        path = Path(path)
        payload = []
        for record in self.records:
            payload.append(
                {
                    "request": {
                        "goal": record.request.goal,
                        "node_name": record.request.node_name,
                        "reason": record.request.reason,
                        "scene_summary": record.request.scene_summary,
                        "memory_snapshot": record.request.memory_snapshot,
                        "spatial_snapshot": record.request.spatial_snapshot,
                        "last_result": asdict(record.request.last_result),
                    },
                    "response": asdict(record.response) if record.response is not None else None,
                }
            )
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


@dataclass
class HumanInTheLoopManager:
    handler: Optional[InterventionHandler] = None
    log: InterventionLog = field(default_factory=InterventionLog)

    def request(self, request: InterventionRequest) -> StepResult | None:
        response = self.handler(request) if self.handler is not None else None
        self.log.add(request, response)
        return response
