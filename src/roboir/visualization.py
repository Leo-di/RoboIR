from __future__ import annotations

from typing import Iterable, Mapping, Any

from .trace import TraceLog


def _step_events_from_trace_log(trace_log: TraceLog) -> list[Mapping[str, Any]]:
    return [event.payload for event in trace_log.events if event.kind == "step"]


def trace_events_to_mermaid(step_events: Iterable[Mapping[str, Any]], title: str = "Trace Flow") -> str:
    lines = ["flowchart TD", f"subgraph {title.replace(' ', '_')}"]
    previous = None
    step_index = 0
    for event in step_events:
        node_name = str(event.get("node", f"step_{step_index}"))
        status = str(event.get("status", "unknown"))
        label = f"{node_name}\\n{status}"
        node_id = f"n{step_index}"
        lines.append(f'{node_id}["{label}"]')
        if previous is not None:
            lines.append(f"{previous} --> {node_id}")
        previous = node_id
        step_index += 1
    lines.append("end")
    return "\n".join(lines)


def trace_to_mermaid(trace_log: TraceLog, title: str = "Trace Flow") -> str:
    return trace_events_to_mermaid(_step_events_from_trace_log(trace_log), title=title)
