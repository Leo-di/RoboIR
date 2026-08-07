from __future__ import annotations

from .base import RobotAdapter
from .mock import MockRobotAdapter
from .sim import IsaacSimAdapter, Ros2Adapter, ScriptedSimAdapter


def build_robot_adapter(name: str) -> RobotAdapter:
    if name == "mock":
        return MockRobotAdapter()
    if name == "sim":
        return ScriptedSimAdapter()
    if name == "ros2":
        return Ros2Adapter()
    if name == "isaac_sim":
        return IsaacSimAdapter()
    available = ", ".join(["mock", "sim", "ros2", "isaac_sim"])
    raise ValueError(f"unknown adapter '{name}'. available: {available}")
