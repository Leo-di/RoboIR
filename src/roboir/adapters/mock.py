from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .base import RobotAdapter, RobotCommand, RobotFeedback, RobotObservation


@dataclass
class MockRobotAdapter:
    name: str = "mock"
    observation: RobotObservation = field(default_factory=lambda: RobotObservation(payload={"status": "idle"}))
    commands: List[RobotCommand] = field(default_factory=list)

    def observe(self) -> RobotObservation:
        return self.observation

    def execute(self, command: RobotCommand) -> RobotFeedback:
        self.commands.append(command)
        return RobotFeedback(success=True, message=f"executed {command.skill_name}", metadata={"command_count": len(self.commands)})

    def reset(self) -> None:
        self.commands.clear()
