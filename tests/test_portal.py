from pathlib import Path
import subprocess
import sys

from roboir.portal import default_portal_index


def test_portal_has_all_sections():
    portal = default_portal_index()
    names = [section.name for section in portal.sections]
    assert names == ["Examples", "Templates", "Adapters", "Task Packs", "Plugins"]


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
