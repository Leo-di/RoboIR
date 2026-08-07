from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .base import RobotAdapter, RobotCommand, RobotFeedback, RobotObservation


@dataclass
class ScriptedSimAdapter:
    name: str = "sim"
    observation_script: List[Dict[str, Any]] = field(default_factory=lambda: [
        {"scene": "desk", "status": "idle"},
        {"scene": "desk", "status": "ready"},
    ])
    feedback_script: List[RobotFeedback] = field(default_factory=lambda: [
        RobotFeedback(success=True, message="simulated execution"),
    ])
    command_log: List[RobotCommand] = field(default_factory=list)
    _observation_index: int = 0
    _feedback_index: int = 0

    def observe(self) -> RobotObservation:
        payload = self.observation_script[min(self._observation_index, len(self.observation_script) - 1)]
        self._observation_index += 1
        return RobotObservation(payload=payload)

    def execute(self, command: RobotCommand) -> RobotFeedback:
        self.command_log.append(command)
        feedback = self.feedback_script[min(self._feedback_index, len(self.feedback_script) - 1)]
        self._feedback_index += 1
        return feedback

    def reset(self) -> None:
        self.command_log.clear()
        self._observation_index = 0
        self._feedback_index = 0


@dataclass
class Ros2Adapter:
    name: str = "ros2"
    namespace: str = "/roboir"

    def observe(self) -> RobotObservation:
        return RobotObservation(payload={"backend": "ros2", "namespace": self.namespace})

    def execute(self, command: RobotCommand) -> RobotFeedback:
        return RobotFeedback(
            success=True,
            message=f"published {command.skill_name}",
            metadata={"backend": "ros2", "namespace": self.namespace, "parameters": command.parameters},
        )

    def reset(self) -> None:
        return None


@dataclass
class IsaacSimAdapter:
    name: str = "isaac_sim"
    stage: str = "default"

    def observe(self) -> RobotObservation:
        return RobotObservation(payload={"backend": "isaac_sim", "stage": self.stage})

    def execute(self, command: RobotCommand) -> RobotFeedback:
        return RobotFeedback(
            success=True,
            message=f"simulated {command.skill_name} in Isaac Sim",
            metadata={"backend": "isaac_sim", "stage": self.stage, "parameters": command.parameters},
        )

    def reset(self) -> None:
        return None
