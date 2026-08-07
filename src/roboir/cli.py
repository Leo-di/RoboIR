from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import TraceAnalyzer
from .report import ExecutionReport
from .suite import TaskSuite
from .tasks import PACK_BUILDERS, build_task_pack, default_task_catalog
from .discovery import discover_entry_point_plugins


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="roboir", description="RoboIR command line interface")
    subparsers = parser.add_subparsers(dest="command", required=True)

    task_choices = sorted(PACK_BUILDERS)

    demo_parser = subparsers.add_parser("demo", help="Run a task pack demo")
    demo_parser.add_argument("--pack", choices=task_choices, default="workcell")

    benchmark_parser = subparsers.add_parser("benchmark", help="Run a task pack benchmark")
    benchmark_parser.add_argument("--pack", choices=task_choices, default="workcell")
    benchmark_parser.add_argument("--json", type=Path, default=None, help="Optional JSON summary output path")

    suite_parser = subparsers.add_parser("suite", help="Run a benchmark suite across multiple packs")
    suite_parser.add_argument("--packs", nargs="+", choices=task_choices, default=task_choices)
    suite_parser.add_argument("--json", type=Path, default=None, help="Optional JSON summary output path")

    export_parser = subparsers.add_parser("export", help="Export a trace dataset from a task pack demo")
    export_parser.add_argument("--pack", choices=task_choices, default="workcell")
    export_parser.add_argument("--output", type=Path, default=Path("trace.jsonl"), help="Output JSONL path")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a trace dataset")
    analyze_parser.add_argument("--input", type=Path, required=True, help="Input JSONL trace dataset")
    analyze_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown report output")

    catalog_parser = subparsers.add_parser("catalog", help="List available task packs")
    catalog_parser.add_argument("--json", type=Path, default=None, help="Optional JSON output path")
    catalog_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown output path")

    plugins_parser = subparsers.add_parser("plugins", help="List discovered plugins")
    plugins_parser.add_argument("--json", type=Path, default=None, help="Optional JSON output path")

    return parser


def _write_output(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in {"demo", "benchmark", "export"}:
        pack = build_task_pack(args.pack)

    if args.command == "demo":
        report = pack.runtime.run_report(goal=pack.name, scene_graph=pack.scene_graph, nodes=pack.plan)
        for result in report.results:
            print(f"{result.status.value}: {result.message}")
        return 0

    if args.command == "benchmark":
        report = pack.benchmark.run(pack.runtime)
        summary = report.summary()
        print(summary)
        if args.json is not None:
            _write_output(args.json, json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    if args.command == "suite":
        suite = TaskSuite()
        for pack_name in args.packs:
            suite.add(pack_name)
        report = suite.run()
        summary = report.summary()
        print(summary)
        if args.json is not None:
            _write_output(args.json, json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        return 0

    if args.command == "export":
        report = pack.runtime.run_report(goal=pack.name, scene_graph=pack.scene_graph, nodes=pack.plan)
        pack.export_dataset(args.output, goal=pack.name)
        print(report.summary())
        print(f"exported dataset to {args.output}")
        return 0

    if args.command == "analyze":
        analyzer = TraceAnalyzer.from_jsonl(args.input)
        report = analyzer.summary()
        print(report.to_dict())
        if args.markdown is not None:
            _write_output(args.markdown, analyzer.to_markdown())
        return 0

    if args.command == "catalog":
        catalog = default_task_catalog()
        print(catalog.to_markdown())
        if args.json is not None:
            _write_output(args.json, json.dumps(catalog.records(), ensure_ascii=False, indent=2))
        if args.markdown is not None:
            _write_output(args.markdown, catalog.to_markdown())
        return 0

    if args.command == "plugins":
        plugins = discover_entry_point_plugins()
        payload = [{"name": plugin.name, "type": plugin.__class__.__name__} for plugin in plugins]
        print(payload)
        if args.json is not None:
            _write_output(args.json, json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
