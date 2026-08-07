from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class AdapterSpec:
    name: str
    kind: str
    description: str
    backend: str


def default_adapter_catalog() -> List[AdapterSpec]:
    return [
        AdapterSpec(name="mock", kind="local", description="fast in-process adapter for tests and demos", backend="mock"),
        AdapterSpec(name="sim", kind="simulator", description="scripted simulator-style adapter", backend="sim"),
        AdapterSpec(name="ros2", kind="middleware", description="ROS2-shaped adapter for runtime integration", backend="ros2"),
        AdapterSpec(name="isaac_sim", kind="simulator", description="Isaac Sim-shaped adapter for robot simulation", backend="isaac_sim"),
    ]

