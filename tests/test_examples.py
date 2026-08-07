from pathlib import Path
import subprocess
import sys

from roboir.examples import default_example_catalog, examples_markdown


def test_examples_catalog_is_grouped():
    examples = default_example_catalog()
    assert {example.category for example in examples} == {"execution", "orchestration", "planning", "recovery", "benchmark"}
    markdown = examples_markdown(examples)
    assert "# RoboIR Examples" in markdown
    assert "| Name | Scenario | Path | Tags | Description |" in markdown
    assert "## Featured" in markdown
    assert "## Categories" in markdown


def test_examples_command_filters_and_exports(tmp_path: Path):
    markdown_path = tmp_path / "examples.md"
    result = subprocess.run(
        [sys.executable, "-m", "roboir", "examples", "--category", "benchmark", "--markdown", str(markdown_path)],
        cwd=Path(__file__).resolve().parent.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    assert markdown_path.exists()
    assert "benchmark_workcell" in result.stdout
    assert "deskservice_orchestration" not in result.stdout
