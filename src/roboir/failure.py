from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from .graph import StepResult


class FailureCategory(str, Enum):
    PERCEPTION = "perception"
    AFFORDANCE = "affordance"
    PLANNING = "planning"
    EXECUTION = "execution"
    RECOVERY = "recovery"
    INTERVENTION = "intervention"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class FailureRecord:
    goal: str
    node_name: str
    category: FailureCategory
    message: str
    artifacts: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FailureLog:
    records: List[FailureRecord] = field(default_factory=list)

    def add(self, goal: str, node_name: str, category: FailureCategory, result: StepResult) -> None:
        self.records.append(
            FailureRecord(
                goal=goal,
                node_name=node_name,
                category=category,
                message=result.message,
                artifacts=result.artifacts,
            )
        )

    def summary(self) -> Dict[str, int]:
        counts = Counter(record.category.value for record in self.records)
        return dict(counts)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "count": len(self.records),
            "summary": self.summary(),
            "records": [
                {
                    "goal": record.goal,
                    "node_name": record.node_name,
                    "category": record.category.value,
                    "message": record.message,
                    "artifacts": record.artifacts,
                }
                for record in self.records
            ],
        }

    def export_json(self, path: str | Path) -> None:
        path = Path(path)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


@dataclass
class FailureClassifier:
    def classify(self, result: StepResult, node_name: str = "", goal: str = "") -> FailureCategory:
        explicit = result.artifacts.get("failure_category")
        if isinstance(explicit, str):
            try:
                return FailureCategory(explicit)
            except ValueError:
                return FailureCategory.UNKNOWN

        text = " ".join(
            [
                goal,
                node_name,
                result.message,
                " ".join(f"{key}:{value}" for key, value in result.artifacts.items()),
            ]
        ).lower()

        if any(token in text for token in ["perception", "detect", "observe", "vision", "scan"]):
            return FailureCategory.PERCEPTION
        if any(token in text for token in ["afford", "grasp", "pick", "place", "contact", "reach"]):
            return FailureCategory.AFFORDANCE
        if any(token in text for token in ["plan", "route", "policy", "schedule", "graph"]):
            return FailureCategory.PLANNING
        if any(token in text for token in ["recover", "retry", "reset", "fallback"]):
            return FailureCategory.RECOVERY
        if any(token in text for token in ["intervention", "human", "handoff"]):
            return FailureCategory.INTERVENTION
        if any(token in text for token in ["exec", "controller", "motor", "hardware"]):
            return FailureCategory.EXECUTION
        return FailureCategory.UNKNOWN
