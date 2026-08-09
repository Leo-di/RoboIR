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
            category="执行",
            scenario="桌面服务执行",
            description="使用适配器完成桌面服务端到端执行",
            tags=("桌面", "服务", "执行"),
            featured=True,
        ),
        ExampleSpec(
            name="deskservice_orchestration",
            path="examples/deskservice_orchestration.py",
            category="编排",
            scenario="图编排",
            description="展示带运行时阶段的规划与执行",
            tags=("图", "规划", "运行时"),
            featured=True,
        ),
        ExampleSpec(
            name="workcell_kitting",
            path="examples/workcell_kitting.py",
            category="规划",
            scenario="工业工位",
            description="展示技能路由与轨迹导出",
            tags=("技能", "可供性", "轨迹"),
            featured=True,
        ),
        ExampleSpec(
            name="recovery_demo",
            path="examples/recovery_demo.py",
            category="恢复",
            scenario="故障恢复",
            description="展示故障与恢复行为",
            tags=("恢复", "验证"),
        ),
        ExampleSpec(
            name="benchmark_workcell",
            path="examples/benchmark_workcell.py",
            category="基准",
            scenario="基准套件",
            description="工位任务包的基准运行",
            tags=("基准", "套件"),
        ),
        ExampleSpec(
            name="benchmark_lab",
            path="examples/benchmark_lab.py",
            category="基准",
            scenario="基准套件",
            description="实验室任务包的基准运行",
            tags=("基准", "套件"),
        ),
        ExampleSpec(
            name="benchmark_office",
            path="examples/benchmark_office.py",
            category="基准",
            scenario="基准套件",
            description="办公任务包的基准运行",
            tags=("基准", "套件"),
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
        f"- 示例数：{len(examples)}",
        f"- 分类：{', '.join(categories)}",
        f"- 场景：{', '.join(scenarios)}",
        f"- 精选数：{len(featured)}",
    ]


def examples_markdown(examples: list[ExampleSpec] | None = None) -> str:
    examples = examples or default_example_catalog()
    featured_examples = [example for example in examples if example.featured]
    lines = [
        "# RoboIR 示例",
        "",
        "这些示例把编排、技能路由、恢复和基准流程串成一个活索引。",
        "",
        "## 快照",
        "",
        *_example_summary(examples),
        "",
        "## 快速开始",
        "",
        "```bash",
        "python examples/run_deskservice.py",
        "roboir examples --category 基准",
        "```",
        "",
        "## 精选",
        "",
        "| 名称 | 场景 | 路径 | 标签 | 说明 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for example in featured_examples:
        tags = ", ".join(f"`{tag}`" for tag in example.tags) if example.tags else "-"
        lines.append(f"| `{example.name}` | `{example.scenario}` | `{example.path}` | {tags} | {example.description} |")
    if not featured_examples:
        lines.append("| - | - | - | - | 暂无精选示例 |")
    lines.extend([
        "",
        "## 索引",
        "",
        "| 名称 | 分类 | 场景 | 路径 | 说明 |",
        "| --- | --- | --- | --- | --- |",
    ])
    for example in examples:
        lines.append(
            f"| `{example.name}` | `{example.category}` | `{example.scenario}` | `{example.path}` | {example.description} |"
        )
    lines.extend([
        "",
        "## 分类",
        "",
    ])
    categories = sorted({example.category for example in examples})
    for category in categories:
        lines.append(f"### {category}")
        for example in [item for item in examples if item.category == category]:
            lines.append(f"- `{example.name}` — `{example.path}`")
        lines.append("")
    lines.extend([
        "## 使用方式",
        "",
        "```bash",
        "python examples/run_deskservice.py",
        "roboir examples --category 基准",
        "```",
    ])
    return "\n".join(lines)


def save_examples_json(path: str | Path, examples: list[ExampleSpec] | None = None) -> None:
    path = Path(path)
    path.write_text(json.dumps(examples_records(examples), ensure_ascii=False, indent=2), encoding="utf-8")
