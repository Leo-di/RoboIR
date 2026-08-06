# RoboIR

`RoboIR` is an embodied intermediate representation for desk-level industrial and service robot tasks.

It sits between perception / VLA policies and robot execution, with a focus on **scene state**, **affordance grounding**, **skill routing**, **graph execution**, **recovery**, and **traceable memory**.

## Why this layer matters

Modern embodied stacks are powerful but fragmented:

- foundation models produce actions or plans
- robot frameworks execute controllers and policies
- task logic is often scattered across prompts, scripts, and ad hoc glue

`RoboIR` proposes a compact middle layer that makes embodied tasks easier to compose, inspect, recover, and reuse across robots and simulators.

## Core concepts

- **SceneGraph** — structured objects and spatial relations
- **AffordanceMap** — candidate actions grounded in the scene
- **SkillRegistry** — reusable skill specifications
- **SkillPlanner** — ranks which skill should fire next
- **GraphRuntime** — executes multi-step embodied workflows
- **RecoveryManager** — applies failure-recovery policies
- **SpatialMemory** — stores object poses and spatial history
- **HumanInTheLoopManager** — records intervention requests and responses
- **TraceLog** — exports execution traces for debugging and dataset creation

## Project layout

```text
src/roboir/
  adapters/      Robot adapter interfaces and mocks
  analysis.py    Trace analysis and reporting
  benchmark.py   Task benchmark primitives
  cli.py         Command line interface
  dataset.py     Trace dataset export/import
  discovery.py   Plugin discovery and loading
  executor.py    Robot-backed embodied executor
  intervention.py Human-in-the-loop request/response handling
  policy.py      Rule-based policy entrypoint
  runtime.py     Runtime orchestration layer
  spatial.py     Spatial memory for poses and history
  suite.py       Multi-pack evaluation suite
  tasks/         Task packs for workcell, lab, office, retail
  visualization.py Trace-to-mermaid conversion
```

## Architecture

```text
RGB / RGB-D / Language
        ↓
  SceneGraph + Memory + SpatialMemory
        ↓
AffordanceMap + SkillPlanner
        ↓
    GraphRuntime / EmbodiedExecutor
        ↓
 RecoveryManager / Intervention / TraceLog
        ↓
 ROS2 / Simulator / Robot
```

## Current scope

This repository now includes:

- scene representation for desk-level tasks
- affordance grounding for pick / place / inspect style actions
- plugin-based skill registration and discovery hooks
- graph-based execution with trace output
- recovery policies and human-in-the-loop intervention hooks
- trace dataset export / import
- benchmark packs for multiple workcell-style tasks
- task suites across multiple packs
- Python-first API and CLI

## Quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .[dev]
roboir demo --pack workcell
roboir benchmark --pack lab
roboir suite --packs workcell lab office retail
roboir export --pack office --output trace.jsonl
roboir analyze --input trace.jsonl --markdown report.md
pytest
```

## Task packs

- `workcell` — kit-style desk manipulation
- `lab` — sample handling and storage
- `office` — fetch and handoff logistics
- `retail` — shelf restock and handoff logistics

## Examples

- [`examples/workcell_kitting.py`](examples/workcell_kitting.py)
- [`examples/recovery_demo.py`](examples/recovery_demo.py)
- [`examples/benchmark_workcell.py`](examples/benchmark_workcell.py)
- [`examples/benchmark_lab.py`](examples/benchmark_lab.py)
- [`examples/benchmark_office.py`](examples/benchmark_office.py)

## Roadmap

- richer affordance grounding
- ROS2 and simulator adapters
- plugin discovery from installed packages
- trace visualization and failure analysis
- more benchmark packs and task suites
- offline learning from execution traces
- human-in-the-loop recovery policies with intervention logging
- benchmark publishing and leaderboard support

## Status

This is an early framework skeleton with multiple task packs and analysis tools. The current goal is to build a practical embodied middle layer that can grow into a larger open-source ecosystem.
