from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TemplateSpec:
    name: str
    kind: str
    path: str
    description: str


def default_template_catalog() -> list[TemplateSpec]:
    return [
        TemplateSpec(name="plugin", kind="extension", path="src/roboir_plugins/template.py", description="copyable plugin skeleton"),
        TemplateSpec(name="adapter", kind="extension", path="src/roboir/adapters/template.py", description="copyable adapter skeleton"),
        TemplateSpec(name="task_pack", kind="extension", path="src/roboir/tasks/template.py", description="copyable task-pack skeleton"),
    ]


def templates_markdown(templates: list[TemplateSpec] | None = None) -> str:
    templates = templates or default_template_catalog()
    lines = [
        "# RoboIR Templates",
        "",
        "These templates are the fastest way to scaffold a downstream RoboIR extension.",
        "",
        "## Overview",
        "",
        "| Name | Kind | Path | Description |",
        "| --- | --- | --- | --- |",
    ]
    for template in templates:
        lines.append(f"| `{template.name}` | `{template.kind}` | `{template.path}` | {template.description} |")
    lines.extend(
        [
            "",
            "## Recommended starting points",
            "",
            "- `plugin` for reusable skills and affordances",
            "- `adapter` for robot or simulator execution backends",
            "- `task_pack` for scene + plan + benchmark bundles",
        ]
    )
    return "\n".join(lines)


def templates_records(templates: list[TemplateSpec] | None = None) -> list[dict[str, object]]:
    templates = templates or default_template_catalog()
    return [template.__dict__ for template in templates]


def save_templates_json(path: str | Path, templates: list[TemplateSpec] | None = None) -> None:
    path = Path(path)
    path.write_text(json.dumps(templates_records(templates), ensure_ascii=False, indent=2), encoding="utf-8")
