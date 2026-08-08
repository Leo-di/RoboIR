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

## Featured entry points

- [`Getting Started`](GETTING_STARTED.md)
- [`Features`](FEATURES.md)
- [`Use Cases`](USE_CASES.md)
- [`Portal`](PORTAL.md)
- [`Examples`](EXAMPLES.md)
- [`Architecture`](ARCHITECTURE.md)
- [`Extending`](EXTENDING.md)

## Best first paths

1. [`Docs Home`](README.md)
2. [`Examples`](EXAMPLES.md)
3. [`Features`](FEATURES.md)
4. [`Use Cases`](USE_CASES.md)
5. [`Portal`](PORTAL.md)

## Repository map

- [`README`](../README.md)
- [`Docs Home`](README.md)
- [`Features`](FEATURES.md)
- [`Use Cases`](USE_CASES.md)
- [`Portal`](PORTAL.md)
- [`Examples`](EXAMPLES.md)
- [`Roadmap`](ROADMAP.md)

## Why this repo exists

Most embodied-AI repos are centered on a model, a benchmark, or a single demo.
RoboIR is centered on the infrastructure layer that ties those parts together.
