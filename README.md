# RoboIR

RoboIR is a modular embodied task infrastructure for desk-level industrial and service robotics.

It is designed as the orchestration layer between perception, VLA policies, planning, execution, recovery, memory, and human intervention.

## What RoboIR is for

- desk-level robot workflows with clear task phases
- skill grounding over scene and affordance signals
- adapter-backed execution against mock, sim, ROS2, and Isaac Sim surfaces
- trace capture for datasets, analysis, and benchmark reports
- plugin-style task packs that can be extended without editing the core stack

If you want a short mental model: `pack + adapter + runtime + trace`.

## Why this repo exists

High-star robotics repos usually win by being immediately usable:

- easy to try
- easy to extend
- easy to reuse

LeRobot is strong on the robot-learning workflow. OpenVLA is strong on VLA training and evaluation. StarVLA is strong on modular code organization.

RoboIR is aimed at the missing middle: a reusable embodied task layer that can ground skills, route execution, recover from failure, and export traces.

## Core building blocks

- `TaskFrame` for phase-aware embodied context
- `SceneGraph` for object-centric grounding
- `AffordanceMap` for action-to-object matching
- `SkillPlanner` for candidate ranking and selection
- `EmbodiedExecutor` for adapter-backed step execution
- `RecoveryManager` and human-in-the-loop intervention hooks
- `TraceLog` and `TraceAnalyzer` for dataset and report export

## Quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .[dev]
roboir catalog
roboir run --pack deskservice --adapter mock
roboir benchmark --pack deskservice
roboir suite --packs workcell lab office retail deskservice
roboir plugins
pytest
```

## First run

```bash
roboir run --pack deskservice --adapter mock --json run.json
```

This prints a compact execution summary and writes a structured report to `run.json`.

## What ships today

- task packs for `workcell`, `lab`, `office`, `retail`, and `deskservice`
- mock, simulator-shaped, ROS2-shaped, and Isaac Sim-shaped adapters
- plugin discovery through entry points and local fallback modules
- benchmark, suite, trace, dataset, and report pipelines
- desk-level embodied task examples with scene, affordance, and skill routing

## Recommended demo pack

`deskservice` is the most representative pack in this repo.
It models a desk-level industrial/service workflow with:

- observe / ground / plan / execute phases
- region-aware affordances
- contact-aware skills
- phased graph execution
- trace and benchmark outputs

## Repository layout

```text
src/roboir/
  embodied.py
  affordance.py
  planner.py
  graph.py
  runtime.py
  executor.py
  benchmark.py
  suite.py
  report.py
  analysis.py
  discovery.py
  adapters/
  tasks/
src/roboir_plugins/
  deskservice.py
docs/
  EXTENDING.md
  GETTING_STARTED.md
  ARCHITECTURE.md
examples/
  run_deskservice.py
  README.md
```

## Examples

- `examples/run_deskservice.py` — end-to-end deskservice execution with a mock adapter
- `examples/deskservice_orchestration.py` — task-frame driven planning and runtime execution
- `examples/workcell_kitting.py` — workcell skill routing and trace export
- `examples/recovery_demo.py` — recovery and intervention demo
- `examples/benchmark_workcell.py` — workcell benchmark run
- `examples/benchmark_lab.py` — lab benchmark run
- `examples/benchmark_office.py` — office benchmark run

Use `roboir examples` for a searchable CLI index.

## Unified Portal

```bash
roboir browse
```

This is the single entry point for examples, templates, adapters, task packs, and plugins.

## Main workflow

1. Load a task pack
2. Pick an adapter
3. Run the embodied graph
4. Inspect trace, failure, and memory outputs
5. Export datasets or benchmark results

## Templates

```bash
roboir templates
```

This lists the copyable plugin, adapter, and task-pack skeletons.

Use `roboir examples` to browse the curated runnable examples.

## Adapter catalog

```bash
roboir adapters
```

Available backends:

- `mock` for fast local tests and demos
- `sim` for scripted simulator-style runs
- `ros2` for ROS2-shaped integration
- `isaac_sim` for Isaac Sim-shaped integration

## Reporting and trace

```bash
roboir report --pack deskservice --json report.json
roboir trace --pack deskservice --markdown trace.md
roboir visualize --pack deskservice --kind scene --output scene.mmd
roboir visualize --pack deskservice --kind trace --markdown trace.md
```

## Scene graph roundtrip

```bash
roboir scene --pack deskservice --output scene.json
roboir scene --input scene.json
```

## Extension points

### Add a task pack

Create a pack under `src/roboir/tasks/` and register it in `src/roboir/tasks/__init__.py`.

For a copyable starting point, use `src/roboir/tasks/template.py`.

### Add a plugin

Ship a plugin module under `src/roboir_plugins/` or expose one through the `roboir.plugins` entry-point group.

### Add an adapter

Implement a new robot adapter under `src/roboir/adapters/` and register it in `src/roboir/adapters/factory.py`.

## Docs

- [`docs/EXTENDING.md`](docs/EXTENDING.md)
- [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md)
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/PORTAL.md`](docs/PORTAL.md)
- [`docs/ROADMAP.md`](docs/ROADMAP.md)
- [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md)
- [`docs/PLUGIN_TEMPLATE.md`](docs/PLUGIN_TEMPLATE.md)
- [`docs/TASK_TEMPLATE.md`](docs/TASK_TEMPLATE.md)
- [`docs/ADAPTER_TEMPLATE.md`](docs/ADAPTER_TEMPLATE.md)

## Status

This is a framework prototype, but it already covers the main layers that mature embodied-AI repos usually need: state, grounding, execution, recovery, traces, datasets, and plug-in task packs.
