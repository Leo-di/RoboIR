from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .affordance import AffordanceMap
from .analysis import TraceAnalyzer
from .embodied import TaskFrame, TaskPhase
from .failure import FailureClassifier, FailureLog
from .graph import GraphNode, GraphRuntime, StepResult
from .intervention import HumanInTheLoopManager, InterventionRequest
from .recovery import RecoveryManager
from .scene import SceneGraph
from .spatial import SpatialMemory
from .report import ExecutionReport
from .trace import TraceLog


@dataclass
class RoboIRRuntime:
    graph_runtime: GraphRuntime
    recovery_manager: RecoveryManager = field(default_factory=RecoveryManager)
    trace_log: TraceLog = field(default_factory=TraceLog)
    spatial_memory: SpatialMemory = field(default_factory=SpatialMemory)
    intervention_manager: HumanInTheLoopManager = field(default_factory=HumanInTheLoopManager)
    failure_classifier: FailureClassifier = field(default_factory=FailureClassifier)
    failure_log: FailureLog = field(default_factory=FailureLog)
    last_report: ExecutionReport | None = None

    @property
    def affordance_map(self) -> AffordanceMap:
        return self.graph_runtime.affordance_map

    def reset(self) -> None:
        self.trace_log = TraceLog()
        self.failure_log = FailureLog()
        self.last_report = None

    def _record_failure(self, goal: str, node_name: str, result: StepResult) -> None:
        category = self.failure_classifier.classify(result, node_name=node_name, goal=goal)
        self.failure_log.add(goal, node_name, category, result)

    def request_intervention(self, goal: str, node_name: str, reason: str, scene_graph: SceneGraph, last_result: StepResult, task_frame: TaskFrame | None = None) -> StepResult | None:
        request = InterventionRequest(
            goal=goal,
            node_name=node_name,
            reason=reason,
            scene_summary=scene_graph.summary(),
            memory_snapshot=self.graph_runtime.memory.snapshot(),
            spatial_snapshot=self.spatial_memory.snapshot(),
            last_result=last_result,
        )
        return self.intervention_manager.request(request)

    def run_report(self, goal: str, scene_graph: SceneGraph, nodes: List[GraphNode], reset: bool = True, task_frame: TaskFrame | None = None) -> ExecutionReport:
        if reset:
            self.reset()
        self.trace_log.add_scene(scene_graph)
        if task_frame is not None:
            self.trace_log.add_task_frame(task_frame)
        results = self.graph_runtime.execute(goal, scene_graph, nodes, task_frame=task_frame)
        final_results: List[StepResult] = []
        context = self.graph_runtime.build_context(goal, scene_graph, task_frame=task_frame)
        for node, result in zip(nodes, results):
            recovered = self.recovery_manager.recover(context, self.graph_runtime.memory, result)
            if recovered.status.name == "FAILED":
                intervention = self.request_intervention(goal, node.name, "recovery_failed", scene_graph, recovered, task_frame=task_frame)
                if intervention is not None:
                    recovered = intervention
            if recovered.status.value == "failed":
                self._record_failure(goal, node.name, recovered)
            self.trace_log.add_step(node.name, recovered, phase=node.phase.value if node.phase is not None else None)
            final_results.append(recovered)
        trace_summary = TraceAnalyzer.from_trace_log(goal=goal, trace_log=self.trace_log, scene_graph=scene_graph, memory_snapshot=self.graph_runtime.memory.snapshot()).summary()
        report = ExecutionReport(goal=goal, results=final_results, trace_summary=trace_summary, failure_log=self.failure_log)
        self.last_report = report
        return report

    def run(self, goal: str, scene_graph: SceneGraph, nodes: List[GraphNode], reset: bool = True, task_frame: TaskFrame | None = None) -> List[StepResult]:
        return self.run_report(goal=goal, scene_graph=scene_graph, nodes=nodes, reset=reset, task_frame=task_frame).results
