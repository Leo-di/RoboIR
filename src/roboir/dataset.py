from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .graph import StepResult
from .scene import SceneGraph
from .trace import TraceLog


@dataclass
class TraceExample:
    goal: str
    scene: Dict[str, Any]
    events: List[Dict[str, Any]]
    memory: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceDataset:
    examples: List[TraceExample] = field(default_factory=list)

    @classmethod
    def from_trace_log(
        cls,
        goal: str,
        scene_graph: SceneGraph,
        trace_log: TraceLog,
        memory_snapshot: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "TraceDataset":
        example = TraceExample(
            goal=goal,
            scene={"summary": scene_graph.summary(), "objects": [asdict(obj) for obj in scene_graph.objects.values()], "relations": [asdict(rel) for rel in scene_graph.relations]},
            events=[asdict(event) for event in trace_log.events],
            memory=memory_snapshot,
            metadata=metadata or {},
        )
        return cls([example])

    def append(self, example: TraceExample) -> None:
        self.examples.append(example)

    def extend(self, examples: Iterable[TraceExample]) -> None:
        self.examples.extend(examples)

    def save_jsonl(self, path: str | Path) -> None:
        path = Path(path)
        with path.open("w", encoding="utf-8") as handle:
            for example in self.examples:
                handle.write(json.dumps(asdict(example), ensure_ascii=False) + "\n")

    @classmethod
    def load_jsonl(cls, path: str | Path) -> "TraceDataset":
        path = Path(path)
        examples: List[TraceExample] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                payload = json.loads(line)
                examples.append(TraceExample(**payload))
        return cls(examples)

    def to_records(self) -> List[Dict[str, Any]]:
        return [asdict(example) for example in self.examples]
