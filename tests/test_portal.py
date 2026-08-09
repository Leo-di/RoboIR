from pathlib import Path
import subprocess
import sys

from roboir.portal import default_portal_index


def test_portal_has_all_sections():
    portal = default_portal_index()
    names = [section.name for section in portal.sections]
    assert names == ["Examples", "Templates", "Adapters", "Task Packs", "Plugins"]
    filtered = portal.with_sections({"Examples", "Templates"})
    assert [section.name for section in filtered.sections] == ["Examples", "Templates"]


def test_browse_command_exports_markdown(tmp_path: Path):
    markdown_path = tmp_path / "portal.md"
    result = subprocess.run(
        [sys.executable, "-m", "roboir", "browse", "--markdown", str(markdown_path)],
        cwd=Path(__file__).resolve().parent.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    assert markdown_path.exists()
    assert "RoboIR Portal" in result.stdout
    assert "Task Packs" in result.stdout


def test_browse_command_can_filter_sections(tmp_path: Path):
    result = subprocess.run(
        [sys.executable, "-m", "roboir", "browse", "--section", "Examples", "--section", "Templates"],
        cwd=Path(__file__).resolve().parent.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "## Examples" in result.stdout
    assert "## Templates" in result.stdout
    assert "## Adapters" not in result.stdout
