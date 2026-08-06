from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional

from .graph import GraphStatus, StepResult
from .memory import TaskMemory
from .skill import SkillContext


RecoveryPolicy = Callable[[SkillContext, TaskMemory, StepResult], StepResult]


@dataclass
class RecoveryManager:
    policies: List[RecoveryPolicy] = field(default_factory=list)

    def add(self, policy: RecoveryPolicy) -> None:
        self.policies.append(policy)

    def recover(self, context: SkillContext, memory: TaskMemory, result: StepResult) -> StepResult:
        if result.status != GraphStatus.FAILED:
            return result
        current = result
        for policy in self.policies:
            current = policy(context, memory, current)
            if current.status != GraphStatus.FAILED:
                return current
        return current
