# RoboIR Examples

Runnable examples for embodied orchestration, skill routing, recovery, and benchmark flows.

## Featured

| Name | Scenario | Path | Description |
| --- | --- | --- | --- |
| `run_deskservice` | desk-service execution | `examples/run_deskservice.py` | end-to-end deskservice execution with an adapter |
| `deskservice_orchestration` | graph orchestration | `examples/deskservice_orchestration.py` | task-frame driven planning and runtime execution |
| `workcell_kitting` | industrial workcell | `examples/workcell_kitting.py` | workcell skill routing and trace export |

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

## Scenarios

### Desk-Service Execution

- `run_deskservice`

### Graph Orchestration

- `deskservice_orchestration`

### Industrial Workcell

- `workcell_kitting`

### Recovery

- `recovery_demo`

### Benchmark

- `benchmark_workcell`
- `benchmark_lab`
- `benchmark_office`

## How to use

```bash
python examples/run_deskservice.py
roboir examples --category benchmark
```
