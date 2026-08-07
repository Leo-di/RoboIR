# Examples

These scripts show the main RoboIR flows in a lightweight way.

## Index

| Name | Category | Path | Description |
| --- | --- | --- | --- |
| `run_deskservice` | `execution` | `examples/run_deskservice.py` | end-to-end deskservice execution with an adapter |
| `deskservice_orchestration` | `orchestration` | `examples/deskservice_orchestration.py` | task-frame driven planning and runtime execution |
| `workcell_kitting` | `planning` | `examples/workcell_kitting.py` | workcell skill routing and trace export |
| `recovery_demo` | `recovery` | `examples/recovery_demo.py` | failure and recovery behavior |
| `benchmark_workcell` | `benchmark` | `examples/benchmark_workcell.py` | benchmark execution for the workcell pack |
| `benchmark_lab` | `benchmark` | `examples/benchmark_lab.py` | benchmark execution for the lab pack |
| `benchmark_office` | `benchmark` | `examples/benchmark_office.py` | benchmark execution for the office pack |

## Categories

### Benchmark

- `benchmark_workcell` — `examples/benchmark_workcell.py`
- `benchmark_lab` — `examples/benchmark_lab.py`
- `benchmark_office` — `examples/benchmark_office.py`

### Execution

- `run_deskservice` — `examples/run_deskservice.py`

### Orchestration

- `deskservice_orchestration` — `examples/deskservice_orchestration.py`

### Planning

- `workcell_kitting` — `examples/workcell_kitting.py`

### Recovery

- `recovery_demo` — `examples/recovery_demo.py`

## How to use

Run them with the project environment active:

```bash
python examples/run_deskservice.py
```

Or browse them from the CLI:

```bash
roboir examples --category benchmark
```
