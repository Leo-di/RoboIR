import subprocess
import sys
from pathlib import Path


def test_templates_command(tmp_path: Path):
    markdown_path = tmp_path / "templates.md"
    result = subprocess.run(
        [sys.executable, "-m", "roboir", "templates", "--markdown", str(markdown_path)],
        cwd=Path(__file__).resolve().parent.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    assert markdown_path.exists()
    assert "task_pack" in result.stdout
