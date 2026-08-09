from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .adapters.catalog import AdapterSpec, default_adapter_catalog
from .discovery import discover_entry_point_plugins
from .examples import ExampleSpec, default_example_catalog
from .plugins import default_deskservice_plugins, default_workcell_plugins
from .tasks.catalog import TaskCatalog, TaskPackSpec, default_task_catalog
from .templates import TemplateSpec, default_template_catalog


@dataclass(frozen=True)
class PortalEntry:
    name: str
    kind: str
    path: str
    description: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PortalSection:
    name: str
    description: str
    entries: tuple[PortalEntry, ...]


@dataclass(frozen=True)
class PortalIndex:
    sections: tuple[PortalSection, ...]

    def with_sections(self, section_names: set[str] | None = None) -> "PortalIndex":
        if not section_names:
            return self
        normalized = {name.lower() for name in section_names}
        filtered_sections = tuple(section for section in self.sections if section.name.lower() in normalized)
        return PortalIndex(sections=filtered_sections)

    def records(self) -> list[dict[str, Any]]:
        return [
            {
                "name": section.name,
                "description": section.description,
                "entries": [
                    {
                        "name": entry.name,
                        "kind": entry.kind,
                        "path": entry.path,
                        "description": entry.description,
                        "metadata": entry.metadata,
                    }
                    for entry in section.entries
                ],
            }
            for section in self.sections
        ]

    def to_markdown(self) -> str:
        section_count = len(self.sections)
        entry_count = sum(len(section.entries) for section in self.sections)
        lines = [
            "# RoboIR 门户",
            "",
            "示例、模板、适配器、任务包和插件的统一索引。",
            "",
            "## 快照",
            "",
            f"- 章节数：{section_count}",
            f"- 条目数：{entry_count}",
            "- 适用场景：快速发现、下游复用和仓库导览",
            "",
            "## 入口",
            "",
            "```bash",
            "roboir examples",
            "roboir templates",
            "roboir adapters",
            "roboir browse",
            "```",
            "",
        ]
        for section in self.sections:
            lines.extend([
                f"## {section.name}",
                "",
                section.description,
                "",
                "| 名称 | 类型 | 路径 | 说明 |",
                "| --- | --- | --- | --- |",
            ])
            for entry in section.entries:
                metadata_hint = ""
                if entry.metadata:
                    metadata_hint = f" <sub>{', '.join(sorted(entry.metadata.keys()))}</sub>"
                lines.append(f"| `{entry.name}` | `{entry.kind}` | `{entry.path}` | {entry.description}{metadata_hint} |")
            lines.append("")
        return "\n".join(lines)


def _example_entries(examples: list[ExampleSpec] | None = None) -> tuple[PortalEntry, ...]:
    examples = examples or default_example_catalog()
    return tuple(
        PortalEntry(name=example.name, kind=example.category, path=example.path, description=example.description)
        for example in examples
    )


def _template_entries(templates: list[TemplateSpec] | None = None) -> tuple[PortalEntry, ...]:
    templates = templates or default_template_catalog()
    return tuple(
        PortalEntry(name=template.name, kind=template.kind, path=template.path, description=template.description)
        for template in templates
    )


def _adapter_entries(adapters: list[AdapterSpec] | None = None) -> tuple[PortalEntry, ...]:
    adapters = adapters or default_adapter_catalog()
    return tuple(
        PortalEntry(name=adapter.name, kind=adapter.kind, path=f"src/roboir/adapters/{adapter.backend}.py", description=adapter.description)
        for adapter in adapters
    )


def _task_entries(task_catalog: TaskCatalog | None = None) -> tuple[PortalEntry, ...]:
    task_catalog = task_catalog or default_task_catalog()
    return tuple(
        PortalEntry(name=spec.name, kind=spec.domain, path=f"src/roboir/tasks/{spec.name}.py", description=spec.description, metadata={"tags": list(spec.tags)})
        for spec in [task_catalog.describe(name) for name in task_catalog.names()]
    )


def _plugin_entries() -> tuple[PortalEntry, ...]:
    plugins = discover_entry_point_plugins()
    fallback_plugins = [default_workcell_plugins(), default_deskservice_plugins()]
    entries: list[PortalEntry] = []
    for plugin in plugins:
        entries.append(
            PortalEntry(
                name=plugin.name,
                kind=plugin.__class__.__name__,
                path=f"entrypoint://{plugin.name}",
                description="已发现的插件入口点",
            )
        )
    if not entries:
        for manager in fallback_plugins:
            for plugin in manager.plugins.values():
                entries.append(
                    PortalEntry(
                        name=plugin.name,
                        kind=plugin.__class__.__name__,
                        path=f"module://{plugin.name}",
                        description="内置插件包",
                    )
                )
    return tuple(entries)


def default_portal_index() -> PortalIndex:
    return PortalIndex(
        sections=(
            PortalSection(
                name="示例",
                description="用于快速验证和演示的可运行脚本。",
                entries=_example_entries(),
            ),
            PortalSection(
                name="模板",
                description="可复制到下游仓库的骨架。",
                entries=_template_entries(),
            ),
            PortalSection(
                name="适配器",
                description="支持的执行后端与运行时表面。",
                entries=_adapter_entries(),
            ),
            PortalSection(
                name="任务包",
                description="把场景、计划和基准打包在一起的内置任务包。",
                entries=_task_entries(),
            ),
            PortalSection(
                name="插件",
                description="可发现的技能与可供性包。",
                entries=_plugin_entries(),
            ),
        ),
    )


def portal_sections() -> list[str]:
    return ["示例", "模板", "适配器", "任务包", "插件"]
