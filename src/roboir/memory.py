from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class MemoryRecord:
    key: str
    value: Any
    source: str


@dataclass
class TaskMemory:
    records: Dict[str, MemoryRecord] = field(default_factory=dict)
    history: List[MemoryRecord] = field(default_factory=list)

    def store(self, key: str, value: Any, source: str) -> None:
        record = MemoryRecord(key=key, value=value, source=source)
        self.records[key] = record
        self.history.append(record)

    def get(self, key: str, default: Any = None) -> Any:
        record = self.records.get(key)
        if record is None:
            return default
        return record.value

    def snapshot(self) -> Dict[str, Any]:
        return {key: record.value for key, record in self.records.items()}
