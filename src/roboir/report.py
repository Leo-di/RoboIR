from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import List

from .analysis import TraceSummary
from .failure import FailureLog
from .graph import StepResult


@dataclass(frozen=True)
class ExecutionReport:
    goal: str
    results: List[StepResult]
    trace_summary: TraceSummary | None = None
    failure_log: FailureLog | None = None

    @property
    def success_count(self) -> int:
        return sum(1 for result in self.results if result.status.value == "success")

    @property
    def failure_count(self) -> int:
        return sum(1 for result in self.results if result.status.value == "failed")

    def summary(self) -> dict[str, object]:
        return {
            "goal": self.goal,
            "result_count": len(self.results),
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "failure_summary": self.failure_log.summary() if self.failure_log is not None else {},
            "trace_summary": self.trace_summary.to_dict() if self.trace_summary is not None else {},
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "goal": self.goal,
            "results": [
                {
                    "status": result.status.value,
                    "message": result.message,
                    "artifacts": result.artifacts,
                }
                for result in self.results
            ],
            "summary": self.summary(),
        }

    def to_markdown(self) -> str:
        summary = self.summary()
        lines = ["# Execution Report", ""]
        for key, value in summary.items():
            lines.append(f"- {key}: {value}")
        lines.append("")
        lines.append("## Results")
        for index, result in enumerate(self.results, start=1):
            lines.append(f"- {index}. `{result.status.value}` — {result.message}")
        return "\n".join(lines)

    def export_json(self, path: str | Path) -> None:
        path = Path(path)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
