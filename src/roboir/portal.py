from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List

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
        lines = ["# RoboIR Portal", "", "A unified index for examples, templates, adapters, tasks, and plugins.", ""]
        for section in self.sections:
            lines.extend([f"## {section.name}", "", section.description, "", "| Name | Kind | Path | Description |", "| --- | --- | --- | --- |"])
            for entry in section.entries:
                lines.append(f"| `{entry.name}` | `{entry.kind}` | `{entry.path}` | {entry.description} |")
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
                description="discovered plugin entry point",
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
                        description="built-in plugin bundle",
                    )
                )
    return tuple(entries)


def default_portal_index() -> PortalIndex:
    return PortalIndex(
        sections=(
            PortalSection(
                name="Examples",
                description="Runnable scripts for quick validation and demos.",
                entries=_example_entries(),
            ),
            PortalSection(
                name="Templates",
                description="Copyable skeletons for downstream repos.",
                entries=_template_entries(),
            ),
            PortalSection(
                name="Adapters",
                description="Supported execution backends and runtime surfaces.",
                entries=_adapter_entries(),
            ),
            PortalSection(
                name="Task Packs",
                description="Built-in task packs that bundle scene, plan, and benchmark.",
                entries=_task_entries(),
            ),
            PortalSection(
                name="Plugins",
                description="Discoverable skill and affordance bundles.",
                entries=_plugin_entries(),
            ),
        ),
    )
