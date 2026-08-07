# RoboIR

RoboIR is a modular embodied orchestration layer for desk-level industrial and service robotics.

It connects perception, VLA policies, planning, execution, recovery, memory, and human intervention into one reusable stack.

[![CI](https://github.com/Leo-di/RoboIR/actions/workflows/ci.yml/badge.svg)](https://github.com/Leo-di/RoboIR/actions/workflows/ci.yml)
[![Issues](https://img.shields.io/github/issues/Leo-di/RoboIR)](https://github.com/Leo-di/RoboIR/issues)
[![PRs](https://img.shields.io/github/issues-pr/Leo-di/RoboIR)](https://github.com/Leo-di/RoboIR/pulls)

## Why this repo exists

Most embodied AI repos stop at a model, a benchmark, or a single demo.
RoboIR focuses on the missing infrastructure layer:

- skill and affordance reuse
- graph-based orchestration
- adapter-backed execution
- trace, benchmark, and dataset export
- plugin-first extension points

## What to try first

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .[dev]
roboir run --pack deskservice --adapter mock
roboir browse
roboir examples
roboir templates
```

## Featured scenarios

- desk-service orchestration
- industrial workcell kitting
- failure recovery and verification
- benchmarkable task packs

## Main entry points

- `roboir run` — execute a task pack with an adapter
- `roboir browse` — unified portal for examples, templates, adapters, task packs, and plugins
- `roboir examples` — runnable example index with scenario filters
- `roboir templates` — copyable extension skeletons
- `roboir catalog` — built-in task pack catalog
- `roboir plugins` — discovered plugin index
- `roboir benchmark` — single-pack benchmark run
- `roboir suite` — multi-pack evaluation sweep

## Portal view

`roboir browse --section Examples --section Templates`

This keeps the repo readable like a real framework homepage, not just a paper code dump.

## Extension model

- task packs bundle scene, plan, and benchmark state
- plugins contribute skills and affordances
- adapters isolate runtime backends
- traces become reports, datasets, and visualizations

## Repository layout

```text
src/roboir/
  cli.py
  portal.py
  examples.py
  templates.py
  tasks/
  adapters/
  graph.py
  runtime.py
  executor.py
  trace.py
  report.py
examples/
docs/
```

## Scenario examples

- `examples/run_deskservice.py` — desk-service execution with a mock adapter
- `examples/deskservice_orchestration.py` — graph-driven orchestration loop
- `examples/workcell_kitting.py` — industrial skill routing and trace export
- `examples/recovery_demo.py` — failure recovery and intervention demo
- `examples/benchmark_workcell.py` — workcell benchmark run

## Docs

- `docs/GETTING_STARTED.md`
- `docs/ARCHITECTURE.md`
- `docs/PORTAL.md`
- `docs/EXTENDING.md`
- `docs/ROADMAP.md`

## Vision

RoboIR aims to be the orchestration and reuse layer for embodied AI — closer to a Hugging Face-style infrastructure repo than a single robot policy implementation.
