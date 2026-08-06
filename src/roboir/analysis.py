from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from .dataset import TraceDataset
from .trace import TraceLog
from .visualization import trace_events_to_mermaid


@dataclass
class TraceSummary:
    task_count: int
    event_count: int
    step_count: int
    status_counts: Dict[str, int]
    goal_counts: Dict[str, int]
    memory_key_counts: Dict[str, int]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_count": self.task_count,
            "event_count": self.event_count,
            "step_count": self.step_count,
            "status_counts": dict(self.status_counts),
            "goal_counts": dict(self.goal_counts),
            "memory_key_counts": dict(self.memory_key_counts),
        }


@dataclass
class TraceAnalyzer:
    dataset: TraceDataset

    @classmethod
    def from_jsonl(cls, path: str | Path) -> "TraceAnalyzer":
        return cls(TraceDataset.load_jsonl(path))

    @classmethod
    def from_trace_log(cls, goal: str, trace_log: TraceLog, scene_graph, memory_snapshot: Dict[str, Any]) -> "TraceAnalyzer":
        dataset = TraceDataset.from_trace_log(goal=goal, scene_graph=scene_graph, trace_log=trace_log, memory_snapshot=memory_snapshot)
        return cls(dataset)

    def summary(self) -> TraceSummary:
        status_counts: Counter[str] = Counter()
        goal_counts: Counter[str] = Counter()
        memory_key_counts: Counter[str] = Counter()
        event_count = 0
        step_count = 0

        for example in self.dataset.examples:
            goal_counts[example.goal] += 1
            event_count += len(example.events)
            for event in example.events:
                if event.get("kind") == "step":
                    step_count += 1
                    status_counts[event["payload"].get("status", "unknown")] += 1
            for key in example.memory:
                memory_key_counts[key] += 1

        return TraceSummary(
            task_count=len(self.dataset.examples),
            event_count=event_count,
            step_count=step_count,
            status_counts=dict(status_counts),
            goal_counts=dict(goal_counts),
            memory_key_counts=dict(memory_key_counts),
        )

    def task_names(self) -> list[str]:
        return [example.goal for example in self.dataset.examples]

    def to_mermaid(self) -> str:
        if not self.dataset.examples:
            return "flowchart TD\nend"
        first = self.dataset.examples[0]
        step_events = [event["payload"] for event in first.events if event.get("kind") == "step"]
        return trace_events_to_mermaid(step_events)

    def to_markdown(self) -> str:
        summary = self.summary()
        lines = [
            "# Trace Summary",
            "",
            f"- tasks: {summary.task_count}",
            f"- events: {summary.event_count}",
            f"- steps: {summary.step_count}",
            "",
            "## Status Counts",
        ]
        for status, count in sorted(summary.status_counts.items()):
            lines.append(f"- {status}: {count}")
        lines.append("")
        lines.append("## Goal Counts")
        for goal, count in sorted(summary.goal_counts.items()):
            lines.append(f"- {goal}: {count}")
        lines.append("")
        lines.append("## Memory Keys")
        for key, count in sorted(summary.memory_key_counts.items()):
            lines.append(f"- {key}: {count}")
        lines.extend(["", "## Mermaid", "", "```mermaid", self.to_mermaid(), "```"])
        return "\n".join(lines)
