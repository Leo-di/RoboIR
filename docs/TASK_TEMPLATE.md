# Task Pack Template

This template shows the smallest useful task-pack surface for RoboIR.

## What a task pack should include

- a scene graph
- a plan graph
- a benchmark suite
- a runtime with plugins installed

## Minimal pattern

```python
from roboir.tasks.template import build_task_pack_template

pack = build_task_pack_template("your_pack_name")
```

## Recommended packaging

- keep the pack domain-specific
- expose one clean builder function
- pair the pack with a plugin module when possible
- add a benchmark case so the pack can be compared consistently
