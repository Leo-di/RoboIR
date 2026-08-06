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
- **TaskMemory** — stores task state and execution history
- **TraceLog** — exports execution traces for debugging and dataset creation

## Architecture

```text
RGB / RGB-D / Language
        ↓
  SceneGraph + Memory
        ↓
AffordanceMap + SkillPlanner
        ↓
    GraphRuntime
        ↓
 RecoveryManager / TraceLog
        ↓
 ROS2 / Simulator / Robot
```

## Current scope

This repository starts small on purpose:

- scene representation for desk-level tasks
- affordance grounding for pick / place / inspect style actions
- plugin-based skill registration
- graph-based execution with trace output
- simple recovery policies
- Python-first API for easy extension

## Quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .[dev]
python examples/workcell_kitting.py
pytest
```

## Minimal API

```python
from roboir import AffordanceMap, GraphNode, GraphRuntime, RoboIRRuntime, SceneGraph, SkillPlanner
```

## Example

See [`examples/workcell_kitting.py`](examples/workcell_kitting.py) for a minimal kitting workflow.

## Roadmap

- richer affordance grounding
- spatial memory with object tracking
- plugin discovery from local packages
- recovery policies with failure types
- ROS2 / sim adapters
- trace export for offline learning
- benchmark packs for desk-level workcells

## Status

This is an early framework skeleton. The current goal is to build a practical embodied middle layer that can be extended into a larger open-source ecosystem.
