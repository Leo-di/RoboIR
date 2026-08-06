from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol


@dataclass(frozen=True)
class RobotObservation:
    payload: Dict[str, Any]


@dataclass(frozen=True)
class RobotCommand:
    skill_name: str
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RobotFeedback:
    success: bool
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class RobotAdapter(Protocol):
    name: str

    def observe(self) -> RobotObservation:
        ...

    def execute(self, command: RobotCommand) -> RobotFeedback:
        ...

    def reset(self) -> None:
        ...
