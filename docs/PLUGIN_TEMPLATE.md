# Plugin Template

This template shows the smallest useful plugin surface for RoboIR.

## What a plugin should provide

- a `PLUGIN` object
- a `build_plugin()` function
- one or more reusable `SkillSpec` entries
- one or more matching `Affordance` entries

## Minimal pattern

```python
from roboir import Affordance, StaticPlugin, SkillSpec, TaskPhase


PLUGIN = StaticPlugin(
    name="your_plugin_name",
    skills=(
        SkillSpec(
            name="your_skill_name",
            description="Describe the reusable skill here",
            satisfies=["inspect"],
            supported_phases=(TaskPhase.OBSERVE.value,),
        ),
    ),
    affordances=(
        Affordance(
            name="your_affordance_name",
            target_category="item",
            action="inspect",
        ),
    ),
)


def build_plugin() -> StaticPlugin:
    return PLUGIN
```

## Recommended packaging

- put the plugin in a small module under `src/`
- expose it through `roboir.plugins` if you want auto-discovery
- keep names domain-specific instead of generic
