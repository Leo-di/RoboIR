from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class TaskPackSpec:
    name: str
    description: str
    domain: str
    tags: tuple[str, ...] = ()


@dataclass
class TaskCatalog:
    specs: Dict[str, TaskPackSpec] = field(default_factory=dict)

    def register(self, spec: TaskPackSpec) -> None:
        self.specs[spec.name] = spec

    def names(self) -> list[str]:
        return sorted(self.specs)

    def describe(self, name: str) -> TaskPackSpec:
        return self.specs[name]

    def records(self) -> list[dict[str, object]]:
        return [asdict(self.specs[name]) for name in self.names()]

    def to_markdown(self) -> str:
        lines = ["# Task Packs", ""]
        for name in self.names():
            spec = self.specs[name]
            lines.append(f"- `{spec.name}` — {spec.description} [{spec.domain}]")
            if spec.tags:
                lines.append(f"  - tags: {', '.join(spec.tags)}")
        return "\n".join(lines)

    def export_json(self, path: str | Path) -> None:
        path = Path(path)
        path.write_text(json.dumps(self.records(), ensure_ascii=False, indent=2), encoding="utf-8")


def default_task_catalog() -> TaskCatalog:
    catalog = TaskCatalog()
    catalog.register(TaskPackSpec(name="workcell", description="Kit-style desk manipulation", domain="industrial-service", tags=("kitting", "desk", "manipulation")))
    catalog.register(TaskPackSpec(name="lab", description="Sample handling and storage", domain="laboratory", tags=("samples", "storage", "sorting")))
    catalog.register(TaskPackSpec(name="office", description="Fetch and handoff logistics", domain="office-service", tags=("handoff", "delivery", "logistics")))
    catalog.register(TaskPackSpec(name="retail", description="Shelf restock and handoff logistics", domain="retail-service", tags=("restock", "shelf", "handoff")))
    catalog.register(TaskPackSpec(name="deskservice", description="Desk-level industrial/service orchestration", domain="desktop-industrial-service", tags=("desk", "orchestration", "multi-step", "handoff")))
    return catalog
