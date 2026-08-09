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
            kind="扩展",
            path="src/roboir_plugins/template.py",
            description="可复制的插件骨架",
            scenario="技能与可供性扩展",
            extension_surface="插件",
            tags=("技能", "可供性", "扩展"),
            featured=True,
        ),
        TemplateSpec(
            name="adapter",
            kind="扩展",
            path="src/roboir/adapters/template.py",
            description="可复制的适配器骨架",
            scenario="后端集成",
            extension_surface="机器人适配器",
            tags=("适配器", "运行时", "后端"),
            featured=True,
        ),
        TemplateSpec(
            name="task_pack",
            kind="扩展",
            path="src/roboir/tasks/template.py",
            description="可复制的任务包骨架",
            scenario="任务 + 场景 + 基准打包",
            extension_surface="任务包",
            tags=("场景", "计划", "基准"),
            featured=True,
        ),
    ]


def templates_markdown(templates: list[TemplateSpec] | None = None) -> str:
    templates = templates or default_template_catalog()
    featured_templates = [template for template in templates if template.featured]
    lines = [
        "# RoboIR 模板",
        "",
        "这些模板是构建下游具身智能集成的最快起点。",
        "",
        "## 快照",
        "",
        f"- 模板数：{len(templates)}",
        f"- 精选数：{len(featured_templates)}",
        f"- 覆盖面：{', '.join(sorted({template.extension_surface for template in templates}))}",
        "",
        "## 推荐起点",
        "",
        "| 名称 | 场景 | 覆盖面 | 路径 | 标签 | 说明 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for template in featured_templates:
        tags = ", ".join(f"`{tag}`" for tag in template.tags) if template.tags else "-"
        lines.append(
            f"| `{template.name}` | `{template.scenario}` | `{template.extension_surface}` | `{template.path}` | {tags} | {template.description} |"
        )
    if not featured_templates:
        lines.append("| - | - | - | - | - | 暂无精选模板 |")
    lines.extend(
        [
            "",
            "## 完整索引",
            "",
            "| 名称 | 类型 | 场景 | 覆盖面 | 路径 | 说明 |",
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
