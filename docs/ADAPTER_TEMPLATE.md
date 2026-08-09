# Adapter Template

This template shows the smallest useful adapter surface for RoboIR.

## What an adapter should provide

- a `name` field
- `observe()` for robot-side state
- `execute(command)` for backend execution
- `reset()` for clean restarts

## Minimal pattern

```python
from roboir.adapters.template import TemplateRobotAdapter

adapter = TemplateRobotAdapter()
```

## Recommended packaging

- keep the adapter backend-specific
- map external system calls into `RobotCommand` and `RobotFeedback`
- keep the adapter free of domain-specific planning logic
