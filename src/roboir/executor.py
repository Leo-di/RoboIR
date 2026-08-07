from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .embodied import TaskFrame
from .failure import FailureCategory
from .graph import GraphNode, GraphStatus, StepResult
from .memory import TaskMemory
from .runtime import RoboIRRuntime
from .scene import SceneGraph
from .adapters.base import RobotAdapter, RobotCommand, RobotFeedback, RobotObservation


@dataclass(frozen=True)
class ExecutionRecord:
    node_name: str
    observation: RobotObservation
    feedback: RobotFeedback
    result: StepResult


@dataclass
class EmbodiedExecutor:
    runtime: RoboIRRuntime
    adapter: RobotAdapter
    records: List[ExecutionRecord] = field(default_factory=list)

    def run(self, goal: str, scene_graph: SceneGraph, nodes: List[GraphNode], task_frame: TaskFrame | None = None) -> List[StepResult]:
        context = self.runtime.graph_runtime.build_context(goal, scene_graph, task_frame=task_frame)
        results: List[StepResult] = []
        current_frame = task_frame
        for node in nodes:
            if current_frame is None and node.phase is not None:
                current_frame = TaskFrame(goal=goal)
            if current_frame is not None and node.phase is not None:
                current_frame = current_frame.advance(node.phase)
            context = self.runtime.graph_runtime.build_context(goal, scene_graph, task_frame=current_frame)
            observation = self.adapter.observe()
            result = node.action(context, self.runtime.graph_runtime.memory)
            feedback = self.adapter.execute(RobotCommand(skill_name=node.skill_name, parameters={"goal": goal, "node": node.name}))
            if not feedback.success and result.status == GraphStatus.SUCCESS:
                result = StepResult(GraphStatus.FAILED, feedback.message, artifacts={"robot_feedback": feedback.metadata})
            if result.status == GraphStatus.FAILED:
                category = self.runtime.failure_classifier.classify(result, node_name=node.name, goal=goal)
                self.runtime.failure_log.add(goal, node.name, category, result)
            self.runtime.graph_runtime.memory.store(node.name, result.message, source=node.skill_name)
            self.runtime.trace_log.add_step(node.name, result, phase=node.phase.value if node.phase is not None else None)
            self.records.append(ExecutionRecord(node_name=node.name, observation=observation, feedback=feedback, result=result))
            results.append(result)
        return results
