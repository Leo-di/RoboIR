from __future__ import annotations

from dataclasses import dataclass, field
import json
from statistics import mean
from pathlib import Path
from typing import List

from .benchmark import BenchmarkReport
from .tasks import build_task_pack


@dataclass(frozen=True)
class SuiteOutcome:
    pack_name: str
    report: BenchmarkReport


@dataclass
class SuiteReport:
    outcomes: List[SuiteOutcome] = field(default_factory=list)

    @property
    def average_score(self) -> float:
        if not self.outcomes:
            return 0.0
        return mean(outcome.report.score for outcome in self.outcomes)

    def summary(self) -> dict[str, float]:
        return {
            "average_score": self.average_score,
            "suite_size": float(len(self.outcomes)),
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "summary": self.summary(),
            "outcomes": [
                {
                    "pack_name": outcome.pack_name,
                    "report": outcome.report.summary(),
                }
                for outcome in self.outcomes
            ],
        }

    def to_markdown(self) -> str:
        lines = ["# Suite Report", ""]
        for key, value in self.summary().items():
            lines.append(f"- {key}: {value}")
        lines.append("")
        lines.append("## Packs")
        for outcome in self.outcomes:
            lines.append(f"- `{outcome.pack_name}` — score {outcome.report.score:.3f}, tasks {len(outcome.report.outcomes)}")
        return "\n".join(lines)

    def export_json(self, path: str | Path) -> None:
        path = Path(path)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


@dataclass
class TaskSuite:
    pack_names: List[str] = field(default_factory=list)

    def add(self, pack_name: str) -> None:
        self.pack_names.append(pack_name)

    def run(self) -> SuiteReport:
        outcomes: List[SuiteOutcome] = []
        for pack_name in self.pack_names:
            pack = build_task_pack(pack_name)
            outcomes.append(SuiteOutcome(pack_name=pack_name, report=pack.benchmark.run(pack.runtime)))
        return SuiteReport(outcomes)
