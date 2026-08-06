from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Sequence


class TaskPhase(str, Enum):
    OBSERVE = "observe"
    GROUND = "ground"
    PLAN = "plan"
    EXECUTE = "execute"
    VERIFY = "verify"
    RECOVER = "recover"
    COMPLETE = "complete"


_PHASE_ORDER = {
    TaskPhase.OBSERVE: 0,
    TaskPhase.GROUND: 1,
    TaskPhase.PLAN: 2,
    TaskPhase.EXECUTE: 3,
    TaskPhase.VERIFY: 4,
    TaskPhase.RECOVER: 5,
    TaskPhase.COMPLETE: 6,
}


@dataclass(frozen=True)
class ContactState:
    object_id: str
    mode: str
    confidence: float = 1.0
    source: str = "policy"


@dataclass(frozen=True)
class RegionConstraint:
    name: str
    spatial_hint: str | None = None
    requires_contact: str | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class TaskFrame:
    goal: str
    pack: str | None = None
    phase: TaskPhase = TaskPhase.OBSERVE
    target_object_ids: tuple[str, ...] = ()
    region_constraints: tuple[RegionConstraint, ...] = ()
    constraints: tuple[str, ...] = ()
    metadata: Dict[str, Any] = field(default_factory=dict)

    def advance(self, phase: TaskPhase) -> "TaskFrame":
        if _PHASE_ORDER[phase] < _PHASE_ORDER[self.phase]:
            raise ValueError(f"cannot move task frame backward from {self.phase.value} to {phase.value}")
        return TaskFrame(
            goal=self.goal,
            pack=self.pack,
            phase=phase,
            target_object_ids=self.target_object_ids,
            region_constraints=self.region_constraints,
            constraints=self.constraints,
            metadata={**self.metadata, "phase": phase.value},
        )

    def summary(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "pack": self.pack,
            "phase": self.phase.value,
            "target_object_ids": list(self.target_object_ids),
            "region_constraints": [
                {
                    "name": constraint.name,
                    "spatial_hint": constraint.spatial_hint,
                    "requires_contact": constraint.requires_contact,
                    "notes": list(constraint.notes),
                }
                for constraint in self.region_constraints
            ],
            "constraints": list(self.constraints),
            "metadata": dict(self.metadata),
        }


@dataclass
class ExecutionFrame:
    goal: str
    task_frame: TaskFrame = field(default_factory=lambda: TaskFrame(goal=""))
    current_phase: TaskPhase = TaskPhase.OBSERVE
    history: List[TaskPhase] = field(default_factory=list)

    def advance(self, phase: TaskPhase) -> None:
        if _PHASE_ORDER[phase] < _PHASE_ORDER[self.current_phase]:
            raise ValueError(f"cannot move execution frame backward from {self.current_phase.value} to {phase.value}")
        self.current_phase = phase
        self.history.append(phase)
        self.task_frame = self.task_frame.advance(phase)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "task_frame": self.task_frame.summary(),
            "current_phase": self.current_phase.value,
            "history": [phase.value for phase in self.history],
        }


@dataclass(frozen=True)
class GroundingDecision:
    object_id: str
    affordance_name: str
    skill_name: str
    score: float
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class TransitionRule:
    from_phase: TaskPhase
    to_phase: TaskPhase
    label: str
    conditions: tuple[str, ...] = ()
    effects: tuple[str, ...] = ()


@dataclass
class TaskStateMachine:
    rules: List[TransitionRule] = field(default_factory=list)
    current_phase: TaskPhase = TaskPhase.OBSERVE
    history: List[TaskPhase] = field(default_factory=list)

    def add_rule(self, rule: TransitionRule) -> None:
        self.rules.append(rule)

    def can_transition(self, to_phase: TaskPhase) -> bool:
        return _PHASE_ORDER[to_phase] >= _PHASE_ORDER[self.current_phase]

    def advance(self, to_phase: TaskPhase) -> None:
        if not self.can_transition(to_phase):
            raise ValueError(f"cannot transition from {self.current_phase.value} to {to_phase.value}")
        self.current_phase = to_phase
        self.history.append(to_phase)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "current_phase": self.current_phase.value,
            "history": [phase.value for phase in self.history],
            "rules": [
                {
                    "from_phase": rule.from_phase.value,
                    "to_phase": rule.to_phase.value,
                    "label": rule.label,
                    "conditions": list(rule.conditions),
                    "effects": list(rule.effects),
                }
                for rule in self.rules
            ],
        }
