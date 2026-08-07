from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class TemplateSpec:
    name: str
    kind: str
    path: str
    description: str
    scenario: str
    extension_surface: str
    tags: tuple[str, ...] = ()
    featured: bool = False


def default_template_catalog() -> list[TemplateSpec]:
    return [
        TemplateSpec(
            name="plugin",
            kind="extension",
            path="src/roboir_plugins/template.py",
            description="copyable plugin skeleton",
            scenario="skill and affordance extension",
            extension_surface="roboir.plugins",
            tags=("skill", "affordance", "extension"),
            featured=True,
        ),
        TemplateSpec(
            name="adapter",
            kind="extension",
            path="src/roboir/adapters/template.py",
            description="copyable adapter skeleton",
            scenario="backend integration",
            extension_surface="robot adapter",
            tags=("adapter", "runtime", "backend"),
            featured=True,
        ),
        TemplateSpec(
            name="task_pack",
            kind="extension",
            path="src/roboir/tasks/template.py",
            description="copyable task-pack skeleton",
            scenario="task + scene + benchmark bundle",
            extension_surface="task pack",
            tags=("scene", "plan", "benchmark"),
            featured=True,
        ),
    ]


def templates_markdown(templates: list[TemplateSpec] | None = None) -> str:
    templates = templates or default_template_catalog()
    featured_templates = [template for template in templates if template.featured]
    lines = [
        "# RoboIR Templates",
        "",
        "Copyable extension points for building downstream embodied AI integrations.",
        "",
        "## Snapshot",
        "",
        f"- templates: {len(templates)}",
        f"- featured: {len(featured_templates)}",
        f"- surfaces: {', '.join(sorted({template.extension_surface for template in templates}))}",
        "",
        "## Recommended starting points",
        "",
        "| Name | Scenario | Surface | Path | Tags | Description |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for template in featured_templates:
        tags = ", ".join(f"`{tag}`" for tag in template.tags) if template.tags else "-"
        lines.append(
            f"| `{template.name}` | `{template.scenario}` | `{template.extension_surface}` | `{template.path}` | {tags} | {template.description} |"
        )
    if not featured_templates:
        lines.append("| - | - | - | - | - | No featured templates configured |")
    lines.extend(
        [
            "",
            "## Full index",
            "",
            "| Name | Kind | Scenario | Surface | Path | Description |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for template in templates:
        lines.append(
            f"| `{template.name}` | `{template.kind}` | `{template.scenario}` | `{template.extension_surface}` | `{template.path}` | {template.description} |"
        )
    return "\n".join(lines)


def templates_records(templates: list[TemplateSpec] | None = None) -> list[dict[str, object]]:
    templates = templates or default_template_catalog()
    return [asdict(template) for template in templates]


def save_templates_json(path: str | Path, templates: list[TemplateSpec] | None = None) -> None:
    path = Path(path)
    path.write_text(json.dumps(templates_records(templates), ensure_ascii=False, indent=2), encoding="utf-8")
