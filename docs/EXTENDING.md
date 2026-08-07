# Extending RoboIR

`RoboIR` is organized around three extension seams:

1. **Plugins** — register reusable skills and affordances
2. **Adapters** — connect execution to simulators or robots
3. **Task packs** — package a domain-specific scene, plan, and benchmark together

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
