# Extending RoboIR

`RoboIR` is organized around three extension seams:

1. **Plugins** — register reusable skills and affordances
2. **Adapters** — connect execution to simulators or robots
3. **Task packs** — package a domain-specific scene, plan, and benchmark together

For a copy-paste plugin skeleton, see [`docs/PLUGIN_TEMPLATE.md`](PLUGIN_TEMPLATE.md).
For a copy-paste task pack skeleton, see [`docs/TASK_TEMPLATE.md`](TASK_TEMPLATE.md) and `src/roboir/tasks/template.py`.
For a copy-paste adapter skeleton, see [`docs/ADAPTER_TEMPLATE.md`](ADAPTER_TEMPLATE.md) and `src/roboir/adapters/template.py`.
Use `roboir templates` to list all template modules in one place.
Use `roboir browse` to see the unified portal for the whole repository.

## Plugin surface

A plugin exposes a `register()` method and can be discovered either from an entry point or by loading a module that exports `PLUGIN` or `build_plugin()`.

Example entry-point target:

```toml
[project.entry-points."roboir.plugins"]
deskservice = "roboir_plugins.deskservice:PLUGIN"
```

## Adapter surface

Adapters implement the `RobotAdapter` protocol:

- `observe()` returns the current robot-side observation
- `execute(command)` sends a skill command and returns feedback
- `reset()` clears adapter state

`RoboIR` ships with `mock`, `sim`, `ros2`, and `isaac_sim`-shaped adapters for development and demos.

## Task packs

Task packs bind together:

- a scene graph
- a plan graph
- a benchmark suite
- a runtime with plugins installed

The `deskservice` pack is the most representative desktop industrial/service example in this repo.

## Template module

`src/roboir_plugins/template.py` is a minimal plugin skeleton you can copy into a downstream repository.

`src/roboir/tasks/template.py` is a minimal task-pack skeleton you can copy into a downstream repository.

`src/roboir/adapters/template.py` is a minimal adapter skeleton you can copy into a downstream repository.

## Where to start

- for a new domain, copy the `deskservice` pack pattern
- for a new backend, add an adapter and register it in the factory
- for a new reusable capability, package it as a plugin
