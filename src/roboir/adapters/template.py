from __future__ import annotations

from dataclasses import dataclass, field

from .base import RobotCommand, RobotFeedback, RobotObservation


@dataclass
class TemplateRobotAdapter:
    name: str = "template"
    observation_payload: dict[str, object] = field(default_factory=lambda: {"backend": "template", "status": "idle"})

    def observe(self) -> RobotObservation:
        return RobotObservation(payload=dict(self.observation_payload))

    def execute(self, command: RobotCommand) -> RobotFeedback:
        return RobotFeedback(
            success=True,
            message=f"template executed {command.skill_name}",
            metadata={"backend": "template", "parameters": command.parameters},
        )

    def reset(self) -> None:
        return None
