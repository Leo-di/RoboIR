from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExampleSpec:
    name: str
    path: str
    category: str
    scenario: str
    description: str
    tags: tuple[str, ...] = ()
    featured: bool = False


def default_example_catalog() -> list[ExampleSpec]:
    return [
        ExampleSpec(
            name="run_deskservice",
            path="examples/run_deskservice.py",
            category="execution",
            scenario="desk-service execution",
            description="end-to-end deskservice execution with an adapter",
            tags=("desk", "service", "execution"),
            featured=True,
        ),
        ExampleSpec(
            name="deskservice_orchestration",
            path="examples/deskservice_orchestration.py",
            category="orchestration",
            scenario="graph orchestration",
            description="task-frame driven planning and runtime execution",
            tags=("graph", "planning", "runtime"),
            featured=True,
        ),
        ExampleSpec(
            name="workcell_kitting",
            path="examples/workcell_kitting.py",
            category="planning",
            scenario="industrial workcell",
            description="workcell skill routing and trace export",
            tags=("skill", "affordance", "trace"),
            featured=True,
        ),
        ExampleSpec(
            name="recovery_demo",
            path="examples/recovery_demo.py",
            category="recovery",
            scenario="failure recovery",
            description="failure and recovery behavior",
            tags=("recovery", "verification"),
        ),
        ExampleSpec(
            name="benchmark_workcell",
            path="examples/benchmark_workcell.py",
            category="benchmark",
            scenario="benchmark suite",
            description="benchmark execution for the workcell pack",
            tags=("benchmark", "suite"),
        ),
        ExampleSpec(
            name="benchmark_lab",
            path="examples/benchmark_lab.py",
            category="benchmark",
            scenario="benchmark suite",
            description="benchmark execution for the lab pack",
            tags=("benchmark", "suite"),
        ),
        ExampleSpec(
            name="benchmark_office",
            path="examples/benchmark_office.py",
            category="benchmark",
            scenario="benchmark suite",
            description="benchmark execution for the office pack",
            tags=("benchmark", "suite"),
        ),
    ]


def examples_records(examples: list[ExampleSpec] | None = None) -> list[dict[str, object]]:
    examples = examples or default_example_catalog()
    return [asdict(example) for example in examples]


def _example_summary(examples: list[ExampleSpec]) -> list[str]:
    categories = sorted({example.category for example in examples})
    scenarios = sorted({example.scenario for example in examples})
    featured = [example for example in examples if example.featured]
    return [
        f"- examples: {len(examples)}",
        f"- categories: {', '.join(categories)}",
        f"- scenarios: {', '.join(scenarios)}",
        f"- featured: {len(featured)}",
    ]


def examples_markdown(examples: list[ExampleSpec] | None = None) -> str:
    examples = examples or default_example_catalog()
    featured_examples = [example for example in examples if example.featured]
    lines = [
        "# RoboIR Examples",
        "",
        "Runnable examples that double as a living index for the framework.",
        "",
        "## Snapshot",
        "",
        *_example_summary(examples),
        "",
        "## Quick start",
        "",
        "```bash",
        "python examples/run_deskservice.py",
        "roboir examples --category benchmark",
        "```",
        "",
        "## Featured",
        "",
        "| Name | Scenario | Path | Tags | Description |",
        "| --- | --- | --- | --- | --- |",
    ]
    for example in featured_examples:
        tags = ", ".join(f"`{tag}`" for tag in example.tags) if example.tags else "-"
        lines.append(f"| `{example.name}` | `{example.scenario}` | `{example.path}` | {tags} | {example.description} |")
    if not featured_examples:
        lines.append("| - | - | - | - | No featured examples configured |")
    lines.extend([
        "",
        "## Index",
        "",
        "| Name | Category | Scenario | Path | Description |",
        "| --- | --- | --- | --- | --- |",
    ])
    for example in examples:
        lines.append(
            f"| `{example.name}` | `{example.category}` | `{example.scenario}` | `{example.path}` | {example.description} |"
        )
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
        "Use the CLI filters to jump to the scenario you care about.",
    ])
    return "\n".join(lines)


def save_examples_json(path: str | Path, examples: list[ExampleSpec] | None = None) -> None:
    path = Path(path)
    path.write_text(json.dumps(examples_records(examples), ensure_ascii=False, indent=2), encoding="utf-8")
