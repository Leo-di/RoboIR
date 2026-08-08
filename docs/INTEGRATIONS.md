# Integrations

RoboIR is intentionally built as a layer that can connect to many embodied AI surfaces.

## Integration map

| Surface | Role in RoboIR | Examples |
| --- | --- | --- |
| Task packs | bundle scene, plan, and benchmark state | `deskservice`, `workcell`, `lab`, `office` |
| Plugins | provide reusable skills and affordances | built-in and entry-point plugins |
| Adapters | connect execution to backends | `mock`, `sim`, `ros2`, `isaac_sim` |
| Traces | preserve runtime behavior for reuse | reports, datasets, benchmark artifacts |
| Docs | guide discovery and extension | `docs/index.md`, `docs/PORTAL.md` |
| Examples | show the canonical workflows | `examples/run_deskservice.py` |
| CLI | expose the high-signal surfaces | `roboir run`, `roboir browse` |

## Common combinations

### Development

- task pack + mock adapter + trace export

### Simulation

- task pack + sim adapter + visualize

### Middleware

- task pack + ROS2-shaped adapter + report export

### Benchmarking

- task pack + benchmark + suite

## Why this matters

The project becomes easier to adopt when each part has a clear integration role.
