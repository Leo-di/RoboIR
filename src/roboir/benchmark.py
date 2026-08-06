from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean
from typing import Callable, Dict, List, Optional

from .graph import GraphNode, GraphStatus, StepResult
from .runtime import RoboIRRuntime
from .scene import SceneGraph


SuccessPredicate = Callable[[List[StepResult], RoboIRRuntime], bool]


@dataclass(frozen=True)
class TaskCase:
    name: str
    goal: str
    scene_graph: SceneGraph
    plan: List[GraphNode]
    success: Optional[SuccessPredicate] = None


@dataclass(frozen=True)
class TaskOutcome:
    name: str
    passed: bool
    results: List[StepResult]


@dataclass
class BenchmarkReport:
    outcomes: List[TaskOutcome] = field(default_factory=list)

    @property
    def score(self) -> float:
        if not self.outcomes:
            return 0.0
        return sum(1 for outcome in self.outcomes if outcome.passed) / len(self.outcomes)

    @property
    def average_steps(self) -> float:
        if not self.outcomes:
            return 0.0
        return mean(len(outcome.results) for outcome in self.outcomes)

    def summary(self) -> Dict[str, float]:
        return {
            "score": self.score,
            "average_steps": self.average_steps,
            "task_count": float(len(self.outcomes)),
        }


@dataclass
class TaskBenchmark:
    cases: List[TaskCase] = field(default_factory=list)

    def add(self, case: TaskCase) -> None:
        self.cases.append(case)

    def run(self, runtime: RoboIRRuntime) -> BenchmarkReport:
        outcomes: List[TaskOutcome] = []
        for case in self.cases:
            results = runtime.run(case.goal, case.scene_graph, case.plan)
            if case.success is None:
                passed = all(result.status != GraphStatus.FAILED for result in results)
            else:
                passed = case.success(results, runtime)
            outcomes.append(TaskOutcome(name=case.name, passed=passed, results=results))
        return BenchmarkReport(outcomes)
