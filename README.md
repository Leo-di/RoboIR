# RoboIR

`RoboIR` is a desk-level embodied intermediate representation for industrial and service robot tasks.

It is designed as the orchestration layer between perception, VLA policies, planning, execution, recovery, memory, and human intervention.

## What it adds

High-star embodied-AI projects usually solve one of four things: data, policies, evaluation, or execution.
`RoboIR` focuses on the missing middle: a reusable task substrate that can ground skills, route execution, recover from failure, and export traces as datasets.

## Core ideas

- **Scene grounding** — object-centric scene graphs and spatial relations
- **Affordance grounding** — action candidates tied to object categories and regions
- **Task frames** — phase-aware execution context for observe / ground / plan / execute / verify / recover
- **Skill routing** — plugin-registered skills scored against task frames and affordances
- **Graph execution** — multi-step embodied workflows with recovery hooks
- **Trace memory** — execution logs that can be turned into datasets and reports
- **Human intervention** — request/response hooks for operator-in-the-loop recovery

## Why this is different

Instead of being only a skill registry or only a benchmark harness, `RoboIR` tries to make embodied tasks composable:

- a planner chooses grounded skills
- a graph runtime executes them in phases
- a runtime records memory, failure, and trace artifacts
- a benchmark suite compares packs across desk-level domains

## Project layout

```text
src/roboir/
  embodied.py     Task frames, phases, and grounded task state
  affordance.py   Affordance definitions and queries
  planner.py      Skill ranking and grounding decisions
  graph.py        Graph nodes and phased execution runtime
  runtime.py      End-to-end orchestration and reporting
  executor.py     Robot adapter-backed execution bridge
  analysis.py     Trace summary and markdown export
  dataset.py      Trace dataset export/import
  plugins.py      Default embodied plugin packs
  tasks/          Domain task packs: workcell, lab, office, retail, deskservice
src/roboir_plugins/
  deskservice.py  Entry-point plugin example for external installs
docs/
  EXTENDING.md    Plugin, adapter, and task-pack extension notes
```

## Quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .[dev]
roboir catalog
roboir demo --pack deskservice
roboir benchmark --pack deskservice
roboir suite --packs workcell lab office retail deskservice
roboir plugins
pytest
```

## Desk-level pack

`deskservice` is the most representative pack for this repo.
It models a desktop industrial/service workflow with:

- observe / ground / plan / execute phases
- region-aware affordances
- contact-mode-aware skills
- routing from pickup zone to transfer lane to tray zone
- traceable memory and benchmarkable multi-step execution

## Adapters and plugins

`RoboIR` now includes adapter stubs for:

- `mock` for tests and examples
- `sim` for scripted simulator-style runs
- `ros2` for ROS-style command publication
- `isaac_sim` for Isaac Sim-shaped integration

It also exposes an entry-point plugin surface so external packs can register skills and affordances without editing the core repo.

## Example

```python
from roboir import RegionConstraint, TaskFrame, TaskPhase, build_task_pack
from roboir.policy import RuleBasedPolicy
from roboir.planner import SkillPlanner

pack = build_task_pack("deskservice")
frame = TaskFrame(
    goal="desk assembly handoff",
    pack="deskservice",
    phase=TaskPhase.OBSERVE,
    target_object_ids=("part_1",),
    region_constraints=(RegionConstraint(name="pickup_zone", spatial_hint="table-left"),),
)
planner = SkillPlanner(pack.runtime.graph_runtime.skill_registry)
policy = RuleBasedPolicy(planner)
decision = policy.decide(pack.scene_graph, pack.runtime.affordance_map, task_frame=frame)
print(decision)
```

## Status

This is a framework prototype, but it already covers the main layers that top embodied-AI repos tend to need: state, grounding, execution, recovery, traces, datasets, and plug-in task packs.
