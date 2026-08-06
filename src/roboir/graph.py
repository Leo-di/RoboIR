from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .affordance import AffordanceMap
from .embodied import TaskFrame, TaskPhase
from .memory import TaskMemory
from .scene import SceneGraph
from .skill import SkillContext, SkillRegistry


class GraphStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    RECOVERED = "recovered"


@dataclass(frozen=True)
class StepResult:
    status: GraphStatus
    message: str
    artifacts: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GraphNode:
    name: str
    skill_name: str
    action: Callable[[SkillContext, TaskMemory], StepResult]
    recovery: Optional[Callable[[SkillContext, TaskMemory, StepResult], StepResult]] = None
    retries: int = 0
    phase: TaskPhase | None = None
    region_hint: str | None = None
    contact_mode: str | None = None


@dataclass
class GraphRuntime:
    skill_registry: SkillRegistry
    affordance_map: AffordanceMap
    memory: TaskMemory = field(default_factory=TaskMemory)

    def build_context(self, goal: str, scene_graph: SceneGraph, task_frame: TaskFrame | None = None) -> SkillContext:
        return SkillContext(goal=goal, scene_graph=scene_graph, task_frame=task_frame, state={"memory": self.memory.snapshot()})

    def execute(self, goal: str, scene_graph: SceneGraph, nodes: List[GraphNode], task_frame: TaskFrame | None = None) -> List[StepResult]:
        results: List[StepResult] = []
        current_frame = task_frame
        for node in nodes:
            if current_frame is None and node.phase is not None:
                current_frame = TaskFrame(goal=goal)
            if current_frame is not None and node.phase is not None:
                current_frame = current_frame.advance(node.phase)
            context = self.build_context(goal, scene_graph, task_frame=current_frame)
            current = node.action(context, self.memory)
            attempt = 0
            while current.status == GraphStatus.FAILED and attempt < node.retries and node.recovery is not None:
                current = node.recovery(context, self.memory, current)
                attempt += 1
            self.memory.store(node.name, current.message, source=node.skill_name)
            results.append(current)
        return results
