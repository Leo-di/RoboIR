# RoboIR Examples

Runnable examples for embodied orchestration, skill routing, recovery, and benchmark flows.

## Quick path

| Path | What it shows | Why it matters |
| --- | --- | --- |
| `examples/run_deskservice.py` | desk-service execution | shortest path to a working demo |
| `examples/deskservice_orchestration.py` | graph orchestration | shows phased orchestration with recovery |
| `examples/workcell_kitting.py` | industrial workcell | shows skill routing and trace export |

## Task guide

### 1. Desk service

Start with the smallest end-to-end flow:

- `run_deskservice` — a complete desk-service run
- `deskservice_orchestration` — graph-based orchestration with runtime phases

### 2. Industrial cell

Move to a more structured embodied workflow:

- `workcell_kitting` — skill routing and trace export
- `benchmark_workcell` — benchmark run for the same pack

### 3. Lab and office

Use the benchmark packs to compare evaluation paths:

- `benchmark_lab`
- `benchmark_office`

### 4. Recovery

Inspect the failure-aware path:

- `recovery_demo` — failure and recovery behavior

## Scenario matrix

| Scenario | Example | Output style |
| --- | --- | --- |
| Desk service | `run_deskservice` | end-to-end execution |
| Graph orchestration | `deskservice_orchestration` | phased planning + verification |
| Industrial workcell | `workcell_kitting` | skill routing + trace export |
| Recovery | `recovery_demo` | failure handling |
| Benchmark | `benchmark_workcell`, `benchmark_lab`, `benchmark_office` | repeatable evaluation |

## Full index

| Name | Category | Scenario | Path | Description |
| --- | --- | --- | --- | --- |
| `run_deskservice` | `execution` | `desk-service execution` | `examples/run_deskservice.py` | end-to-end deskservice execution with an adapter |
| `deskservice_orchestration` | `orchestration` | `graph orchestration` | `examples/deskservice_orchestration.py` | task-frame driven planning and runtime execution |
| `workcell_kitting` | `planning` | `industrial workcell` | `examples/workcell_kitting.py` | workcell skill routing and trace export |
| `recovery_demo` | `recovery` | `failure recovery` | `examples/recovery_demo.py` | failure and recovery behavior |
| `benchmark_workcell` | `benchmark` | `benchmark suite` | `examples/benchmark_workcell.py` | benchmark execution for the workcell pack |
| `benchmark_lab` | `benchmark` | `benchmark suite` | `examples/benchmark_lab.py` | benchmark execution for the lab pack |
| `benchmark_office` | `benchmark` | `benchmark suite` | `examples/benchmark_office.py` | benchmark execution for the office pack |

## How to use

```bash
python examples/run_deskservice.py
roboir examples --category benchmark
```
