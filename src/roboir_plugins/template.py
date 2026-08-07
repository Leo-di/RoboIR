from __future__ import annotations

from roboir import Affordance, StaticPlugin, SkillSpec, TaskPhase


PLUGIN = StaticPlugin(
    name="roboir_template_plugin",
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
            region_hint="workspace",
        ),
    ),
)


def build_plugin() -> StaticPlugin:
    return PLUGIN


def plugin_metadata() -> dict[str, object]:
    return {
        "name": PLUGIN.name,
        "skills": [skill.name for skill in PLUGIN.skills],
        "affordances": [affordance.name for affordance in PLUGIN.affordances],
        "purpose": "copy this module into a downstream package and replace the placeholder names",
    }
