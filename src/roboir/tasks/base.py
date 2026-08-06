from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from ..benchmark import TaskBenchmark
from ..dataset import TraceDataset
from ..graph import GraphNode
from ..runtime import RoboIRRuntime
from ..scene import SceneGraph


@dataclass
class TaskPack:
    name: str
    runtime: RoboIRRuntime
    scene_graph: SceneGraph
    plan: List[GraphNode]
    benchmark: TaskBenchmark

    def export_dataset(self, path: str | Path, goal: str | None = None) -> None:
        dataset = TraceDataset.from_trace_log(
            goal=goal or self.name,
            scene_graph=self.scene_graph,
            trace_log=self.runtime.trace_log,
            memory_snapshot=self.runtime.graph_runtime.memory.snapshot(),
            metadata={"pack": self.name},
        )
        dataset.save_jsonl(path)
