from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .affordance import AffordanceMap
from .graph import GraphNode, GraphRuntime, StepResult
from .recovery import RecoveryManager
from .scene import SceneGraph
from .trace import TraceLog


@dataclass
class RoboIRRuntime:
    graph_runtime: GraphRuntime
    recovery_manager: RecoveryManager = field(default_factory=RecoveryManager)
    trace_log: TraceLog = field(default_factory=TraceLog)

    @property
    def affordance_map(self) -> AffordanceMap:
        return self.graph_runtime.affordance_map

    def run(self, goal: str, scene_graph: SceneGraph, nodes: List[GraphNode]) -> List[StepResult]:
        self.trace_log.add_scene(scene_graph)
        results = self.graph_runtime.execute(goal, scene_graph, nodes)
        final_results: List[StepResult] = []
        context = self.graph_runtime.build_context(goal, scene_graph)
        for node, result in zip(nodes, results):
            recovered = self.recovery_manager.recover(context, self.graph_runtime.memory, result)
            self.trace_log.add_step(node.name, recovered)
            final_results.append(recovered)
        return final_results
