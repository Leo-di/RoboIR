# RoboIR

Modular embodied orchestration for desk-level industrial and service robotics.

RoboIR turns embodied AI workflows into reusable infrastructure: task packs, plugins, adapters, traces, and graph-based execution.

## Quick start

```bash
roboir run --pack deskservice --adapter mock
roboir browse
roboir examples
roboir templates
```

## What RoboIR gives you

- **Task packs** for packaging scenario, scene, plan, and benchmark data
- **Plugins** for reusable skills and affordances
- **Adapters** for mock, sim, ROS2, and Isaac Sim-shaped surfaces
- **Orchestration** for graph-based planning, verification, and recovery
- **Traces** for reporting, datasets, and evaluation reuse

## Core use cases

- desk-service orchestration
- industrial workcell kitting
- failure recovery and intervention
- benchmarkable embodied workflows

## Start here

1. [`Getting Started`](GETTING_STARTED.md)
2. [`Portal`](PORTAL.md)
3. [`Examples`](EXAMPLES.md)
4. [`Architecture`](ARCHITECTURE.md)
5. [`Extending`](EXTENDING.md)

## Repository map

- [`README`](../README.md)
- [`Docs Home`](README.md)
- [`Portal`](PORTAL.md)
- [`Examples`](EXAMPLES.md)
- [`Roadmap`](ROADMAP.md)

## Why this repo exists

Most embodied-AI repos are centered on a model, a benchmark, or a single demo.
RoboIR is centered on the infrastructure layer that ties those parts together.
