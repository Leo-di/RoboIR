# Architecture

RoboIR is organized as a small embodied orchestration stack for desk-level industrial and service robotics.

The design goal is to keep the framework usable as infrastructure, not as a one-off demo.

## Data flow

```text
Scene + TaskFrame
    ↓
AffordanceMap
    ↓
SkillPlanner
    ↓
GraphRuntime
    ↓
EmbodiedExecutor
    ↓
Trace / Failure / Memory
```

## Core layers

- `SceneGraph` stores object-centric state
- `AffordanceMap` grounds action opportunities
- `SkillPlanner` ranks skill candidates for a task frame
- `GraphRuntime` executes phased graph nodes
- `EmbodiedExecutor` bridges runtime logic to adapters
- `RecoveryManager` and `HumanInTheLoopManager` handle failure recovery
- `TraceLog` and `TraceAnalyzer` turn executions into artifacts
- `SceneGraph.save_json()` and `SceneGraph.load_json()` make scene state portable
- `default_adapter_catalog()` exposes the supported backend surface
- `scene_graph_to_mermaid()` and `trace_to_mermaid()` render lightweight diagrams

## Extension model

RoboIR is intentionally plugin-first:

- task packs bundle scene, plan, and benchmark
- plugins register skills and affordances
- adapters isolate the backend execution surface
- reports and datasets are generated from the same runtime trace

## What this enables

- reusable skill libraries for embodied tasks
- graph-driven orchestration instead of single-shot prompting
- adapter-backed execution for mock, sim, and robot surfaces
- traceable outputs that support evaluation and downstream reuse
