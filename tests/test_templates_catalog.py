from pathlib import Path
import subprocess
import sys

from roboir.templates import default_template_catalog, templates_markdown


def test_templates_catalog_uses_table():
    templates = default_template_catalog()
    markdown = templates_markdown(templates)
    assert "| Name | Kind | Path | Description |" in markdown
    assert "Recommended starting points" in markdown


def test_templates_command_exports_markdown(tmp_path: Path):
    markdown_path = tmp_path / "templates.md"
    result = subprocess.run(
        [sys.executable, "-m", "roboir", "templates", "--markdown", str(markdown_path)],
        cwd=Path(__file__).resolve().parent.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    assert markdown_path.exists()
    assert "| Name | Kind | Path | Description |" in result.stdout
