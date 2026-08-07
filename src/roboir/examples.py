from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExampleSpec:
    name: str
    path: str
    category: str
    description: str


def default_example_catalog() -> list[ExampleSpec]:
    return [
        ExampleSpec(name="run_deskservice", path="examples/run_deskservice.py", category="execution", description="end-to-end deskservice execution with an adapter"),
        ExampleSpec(name="deskservice_orchestration", path="examples/deskservice_orchestration.py", category="orchestration", description="task-frame driven planning and runtime execution"),
        ExampleSpec(name="workcell_kitting", path="examples/workcell_kitting.py", category="planning", description="workcell skill routing and trace export"),
        ExampleSpec(name="recovery_demo", path="examples/recovery_demo.py", category="recovery", description="failure and recovery behavior"),
        ExampleSpec(name="benchmark_workcell", path="examples/benchmark_workcell.py", category="benchmark", description="benchmark execution for the workcell pack"),
        ExampleSpec(name="benchmark_lab", path="examples/benchmark_lab.py", category="benchmark", description="benchmark execution for the lab pack"),
        ExampleSpec(name="benchmark_office", path="examples/benchmark_office.py", category="benchmark", description="benchmark execution for the office pack"),
    ]


def examples_records(examples: list[ExampleSpec] | None = None) -> list[dict[str, object]]:
    examples = examples or default_example_catalog()
    return [example.__dict__ for example in examples]


def examples_markdown(examples: list[ExampleSpec] | None = None) -> str:
    examples = examples or default_example_catalog()
    lines = [
        "# Examples",
        "",
        "These scripts show the main RoboIR flows in a lightweight way.",
        "",
        "## Index",
        "",
        "| Name | Category | Path | Description |",
        "| --- | --- | --- | --- |",
    ]
    for example in examples:
        lines.append(f"| `{example.name}` | `{example.category}` | `{example.path}` | {example.description} |")
    lines.extend([
        "",
        "## Categories",
        "",
    ])
    categories = sorted({example.category for example in examples})
    for category in categories:
        lines.append(f"### {category.title()}")
        for example in [item for item in examples if item.category == category]:
            lines.append(f"- `{example.name}` — `{example.path}`")
        lines.append("")
    lines.extend([
        "## How to use",
        "",
        "Run them with the project environment active:",
        "",
        "```bash",
        "python examples/run_deskservice.py",
        "```",
        "",
        "Or browse them from the CLI:",
        "",
        "```bash",
        "roboir examples --category benchmark",
        "```",
    ])
    return "\n".join(lines)


def save_examples_json(path: str | Path, examples: list[ExampleSpec] | None = None) -> None:
    path = Path(path)
    path.write_text(json.dumps(examples_records(examples), ensure_ascii=False, indent=2), encoding="utf-8")
