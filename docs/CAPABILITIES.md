# Capabilities

RoboIR is built as a reusable embodied orchestration layer.

## Capability matrix

| Capability | What it covers | Primary surface |
| --- | --- | --- |
| Orchestration | graph-based planning, verification, and recovery | `roboir run`, `docs/FEATURES.md` |
| Reuse | skills, affordances, task packs, and traces | `roboir templates`, `roboir browse` |
| Execution | mock, sim, ROS2, and Isaac Sim-shaped backends | adapters |
| Discovery | examples, templates, adapters, task packs, plugins | `roboir browse`, `roboir examples` |
| Evaluation | traces, reports, benchmarks, and suites | `roboir benchmark`, `roboir suite` |

## Common flows

- load a task pack
- pick an adapter
- execute a phased graph
- export trace or report artifacts
- reuse the same pack in benchmarking

## Why this matters

A strong embodied-AI framework should not only run a task.
It should make the task reproducible, inspectable, and reusable.
