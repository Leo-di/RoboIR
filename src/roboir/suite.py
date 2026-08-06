from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean
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
