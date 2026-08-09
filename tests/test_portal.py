from pathlib import Path
import subprocess
import sys

from roboir.portal import default_portal_index


def test_portal_has_all_sections():
    portal = default_portal_index()
    names = [section.name for section in portal.sections]
    assert names == ["示例", "模板", "适配器", "任务包", "插件"]
    filtered = portal.with_sections({"示例", "模板"})
    assert [section.name for section in filtered.sections] == ["示例", "模板"]


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
    assert "RoboIR 门户" in result.stdout
    assert "任务包" in result.stdout


def test_browse_command_can_filter_sections(tmp_path: Path):
    result = subprocess.run(
        [sys.executable, "-m", "roboir", "browse", "--section", "示例", "--section", "模板"],
        cwd=Path(__file__).resolve().parent.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "## 示例" in result.stdout
    assert "## 模板" in result.stdout
    assert "## 适配器" not in result.stdout
