from pathlib import Path
import subprocess
import sys

from roboir.examples import default_example_catalog, examples_markdown


def test_examples_catalog_is_grouped():
    examples = default_example_catalog()
    assert {example.category for example in examples} == {"执行", "编排", "规划", "恢复", "基准"}
    markdown = examples_markdown(examples)
    assert "# RoboIR 示例" in markdown
    assert "| 名称 | 场景 | 路径 | 标签 | 说明 |" in markdown
    assert "## 精选" in markdown
    assert "## 分类" in markdown


def test_examples_command_filters_and_exports(tmp_path: Path):
    markdown_path = tmp_path / "examples.md"
    result = subprocess.run(
        [sys.executable, "-m", "roboir", "examples", "--category", "基准", "--markdown", str(markdown_path)],
        cwd=Path(__file__).resolve().parent.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    assert markdown_path.exists()
    assert "benchmark_workcell" in result.stdout
    assert "deskservice_orchestration" not in result.stdout
