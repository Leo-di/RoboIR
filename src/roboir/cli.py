from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adapters.factory import build_robot_adapter
from .adapters.catalog import default_adapter_catalog
from .analysis import TraceAnalyzer
from .embodied import TaskFrame, TaskPhase
from .executor import EmbodiedExecutor
from .examples import default_example_catalog, examples_markdown, examples_records
from .report import ExecutionReport
from .portal import default_portal_index
from .scene import SceneGraph
from .suite import TaskSuite
from .templates import default_template_catalog, templates_markdown, templates_records
from .tasks import PACK_BUILDERS, build_task_pack, default_task_catalog
from .discovery import discover_entry_point_plugins
from .visualization import scene_graph_to_mermaid, trace_to_mermaid


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="roboir", description="RoboIR command line interface")
    subparsers = parser.add_subparsers(dest="command", required=True)

    task_choices = sorted(PACK_BUILDERS)

    demo_parser = subparsers.add_parser("demo", help="Run a task pack demo")
    demo_parser.add_argument("--pack", choices=task_choices, default="workcell")
    demo_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown report output")

    benchmark_parser = subparsers.add_parser("benchmark", help="Run a task pack benchmark")
    benchmark_parser.add_argument("--pack", choices=task_choices, default="workcell")
    benchmark_parser.add_argument("--json", type=Path, default=None, help="Optional JSON summary output path")
    benchmark_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown summary output")

    run_parser = subparsers.add_parser("run", help="Run a task pack with an adapter")
    run_parser.add_argument("--pack", choices=task_choices, default="deskservice")
    run_parser.add_argument("--adapter", choices=["mock", "sim", "ros2", "isaac_sim"], default="mock")
    run_parser.add_argument("--json", type=Path, default=None, help="Optional JSON report output path")
    run_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown report output")

    suite_parser = subparsers.add_parser("suite", help="Run a benchmark suite across multiple packs")
    suite_parser.add_argument("--packs", nargs="+", choices=task_choices, default=task_choices)
    suite_parser.add_argument("--json", type=Path, default=None, help="Optional JSON summary output path")
    suite_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown summary output")

    export_parser = subparsers.add_parser("export", help="Export a trace dataset from a task pack demo")
    export_parser.add_argument("--pack", choices=task_choices, default="workcell")
    export_parser.add_argument("--output", type=Path, default=Path("trace.jsonl"), help="Output JSONL path")
    export_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown report output")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a trace dataset")
    analyze_parser.add_argument("--input", type=Path, required=True, help="Input JSONL trace dataset")
    analyze_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown report output")

    catalog_parser = subparsers.add_parser("catalog", help="List available task packs")
    catalog_parser.add_argument("--json", type=Path, default=None, help="Optional JSON output path")
    catalog_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown output path")

    plugins_parser = subparsers.add_parser("plugins", help="List discovered plugins")
    plugins_parser.add_argument("--json", type=Path, default=None, help="Optional JSON output path")
    plugins_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown output path")

    scene_parser = subparsers.add_parser("scene", help="Export or inspect a scene graph")
    scene_parser.add_argument("--pack", choices=task_choices, default="deskservice")
    scene_parser.add_argument("--output", type=Path, default=None, help="Optional JSON scene output path")
    scene_parser.add_argument("--input", type=Path, default=None, help="Optional JSON scene input path")
    scene_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown output path")

    adapters_parser = subparsers.add_parser("adapters", help="List available adapter backends")
    adapters_parser.add_argument("--json", type=Path, default=None, help="Optional JSON output path")
    adapters_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown output path")

    templates_parser = subparsers.add_parser("templates", help="List copyable template modules")
    templates_parser.add_argument("--json", type=Path, default=None, help="Optional JSON output path")
    templates_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown output path")

    examples_parser = subparsers.add_parser("examples", help="List curated examples")
    examples_parser.add_argument("--category", choices=sorted({example.category for example in default_example_catalog()}), default=None, help="Optional category filter")
    examples_parser.add_argument("--json", type=Path, default=None, help="Optional JSON output path")
    examples_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown output path")

    browse_parser = subparsers.add_parser("browse", help="Browse the unified RoboIR portal")
    browse_parser.add_argument("--json", type=Path, default=None, help="Optional JSON output path")
    browse_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown output path")

    report_parser = subparsers.add_parser("report", help="Run a task pack and export a report")
    report_parser.add_argument("--pack", choices=task_choices, default="deskservice")
    report_parser.add_argument("--json", type=Path, default=None, help="Optional JSON report output path")
    report_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown report output path")

    trace_parser = subparsers.add_parser("trace", help="Run a task pack and export its trace")
    trace_parser.add_argument("--pack", choices=task_choices, default="deskservice")
    trace_parser.add_argument("--json", type=Path, default=None, help="Optional JSON trace output path")
    trace_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown trace output path")

    visualize_parser = subparsers.add_parser("visualize", help="Render a scene or trace as Mermaid")
    visualize_parser.add_argument("--pack", choices=task_choices, default="deskservice")
    visualize_parser.add_argument("--kind", choices=["scene", "trace"], default="scene")
    visualize_parser.add_argument("--output", type=Path, default=None, help="Optional Mermaid output path")
    visualize_parser.add_argument("--markdown", type=Path, default=None, help="Optional markdown output path")

    return parser


def _write_output(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in {"demo", "benchmark", "export", "run", "report", "trace", "scene", "visualize"}:
        pack = build_task_pack(args.pack)

    if args.command == "demo":
        report = pack.runtime.run_report(goal=pack.name, scene_graph=pack.scene_graph, nodes=pack.plan)
        for result in report.results:
            print(f"{result.status.value}: {result.message}")
        if args.markdown is not None:
            _write_output(args.markdown, report.to_markdown())
        return 0

    if args.command == "benchmark":
        report = pack.benchmark.run(pack.runtime)
        summary = report.summary()
        print(summary)
        if args.json is not None:
            _write_output(args.json, json.dumps(summary, ensure_ascii=False, indent=2))
        if args.markdown is not None:
            _write_output(args.markdown, report.to_markdown())
        return 0

    if args.command == "run":
        adapter = build_robot_adapter(args.adapter)
        pack.runtime.reset()
        adapter.reset()
        executor = EmbodiedExecutor(runtime=pack.runtime, adapter=adapter)
        frame = TaskFrame(goal=pack.name, pack=pack.name, phase=TaskPhase.OBSERVE)
        pack.runtime.trace_log.add_scene(pack.scene_graph)
        pack.runtime.trace_log.add_task_frame(frame)
        results = executor.run(goal=pack.name, scene_graph=pack.scene_graph, nodes=pack.plan, task_frame=frame)
        trace_summary = TraceAnalyzer.from_trace_log(
            goal=pack.name,
            trace_log=pack.runtime.trace_log,
            scene_graph=pack.scene_graph,
            memory_snapshot=pack.runtime.graph_runtime.memory.snapshot(),
        ).summary()
        report = ExecutionReport(goal=pack.name, results=results, trace_summary=trace_summary, failure_log=pack.runtime.failure_log)
        payload = {
            "adapter": args.adapter,
            "pack": pack.name,
            "results": [result.status.value for result in results],
            "summary": report.summary(),
        }
        print(
            f"run complete: pack={pack.name} adapter={args.adapter} "
            f"steps={report.summary()['result_count']} "
            f"success={report.success_count} failure={report.failure_count}"
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if args.json is not None:
            _write_output(args.json, json.dumps(payload, ensure_ascii=False, indent=2))
        if args.markdown is not None:
            _write_output(args.markdown, report.to_markdown())
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
        if args.markdown is not None:
            _write_output(args.markdown, report.to_markdown())
        return 0

    if args.command == "export":
        report = pack.runtime.run_report(goal=pack.name, scene_graph=pack.scene_graph, nodes=pack.plan)
        pack.export_dataset(args.output, goal=pack.name)
        print(report.summary())
        print(f"exported dataset to {args.output}")
        if args.markdown is not None:
            _write_output(args.markdown, report.to_markdown())
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
        if args.markdown is not None:
            lines = ["# Discovered Plugins", ""]
            for plugin in plugins:
                lines.append(f"- `{plugin.name}` — {plugin.__class__.__name__}")
            _write_output(args.markdown, "\n".join(lines))
        return 0

    if args.command == "scene":
        if args.input is not None:
            scene_graph = SceneGraph.load_json(args.input)
        else:
            pack = build_task_pack(args.pack)
            scene_graph = pack.scene_graph
        payload = scene_graph.to_dict()
        print(payload)
        if args.output is not None:
            scene_graph.save_json(args.output)
        if args.markdown is not None:
            lines = ["# Scene Graph", ""]
            summary = payload["summary"]
            lines.extend(
                [
                    f"- object_count: {summary['object_count']}",
                    f"- relation_count: {summary['relation_count']}",
                    f"- categories: {', '.join(summary['categories']) if summary['categories'] else 'none'}",
                    "",
                    "## Objects",
                ]
            )
            for item in payload["objects"]:
                lines.append(f"- `{item['object_id']}` — {item['label']} ({item['category']})")
            lines.extend(["", "## Relations"])
            for item in payload["relations"]:
                lines.append(f"- `{item['subject_id']}` {item['predicate']} `{item['object_id']}`")
            _write_output(args.markdown, "\n".join(lines))
        return 0

    if args.command == "adapters":
        adapters = default_adapter_catalog()
        payload = [adapter.__dict__ for adapter in adapters]
        print(payload)
        if args.json is not None:
            _write_output(args.json, json.dumps(payload, ensure_ascii=False, indent=2))
        if args.markdown is not None:
            lines = ["# Adapter Catalog", ""]
            for adapter in adapters:
                lines.append(f"- `{adapter.name}` — {adapter.kind}: {adapter.description}")
            _write_output(args.markdown, "\n".join(lines))
        return 0

    if args.command == "report":
        report = pack.runtime.run_report(goal=pack.name, scene_graph=pack.scene_graph, nodes=pack.plan)
        payload = report.to_dict()
        print(report.to_markdown())
        if args.json is not None:
            _write_output(args.json, json.dumps(payload, ensure_ascii=False, indent=2))
        if args.markdown is not None:
            _write_output(args.markdown, report.to_markdown())
        return 0

    if args.command == "trace":
        pack.runtime.run(goal=pack.name, scene_graph=pack.scene_graph, nodes=pack.plan)
        analyzer = TraceAnalyzer.from_trace_log(
            goal=pack.name,
            trace_log=pack.runtime.trace_log,
            scene_graph=pack.scene_graph,
            memory_snapshot=pack.runtime.graph_runtime.memory.snapshot(),
        )
        trace_log = pack.runtime.trace_log
        payload = [event.__dict__ for event in trace_log.events]
        print(analyzer.to_markdown())
        if args.json is not None:
            _write_output(args.json, json.dumps(payload, ensure_ascii=False, indent=2))
        if args.markdown is not None:
            _write_output(args.markdown, analyzer.to_markdown())
        return 0

    if args.command == "visualize":
        if args.kind == "scene":
            mermaid = scene_graph_to_mermaid(pack.scene_graph, title=f"{pack.name} Scene")
        else:
            pack.runtime.run(goal=pack.name, scene_graph=pack.scene_graph, nodes=pack.plan)
            mermaid = trace_to_mermaid(pack.runtime.trace_log, title=f"{pack.name} Trace")
        print("```mermaid")
        print(mermaid)
        print("```")
        if args.output is not None:
            _write_output(args.output, mermaid)
        if args.markdown is not None:
            _write_output(args.markdown, f"```mermaid\n{mermaid}\n```")
        return 0

    if args.command == "templates":
        templates = default_template_catalog()
        payload = templates_records(templates)
        print(templates_markdown(templates))
        if args.json is not None:
            _write_output(args.json, json.dumps(payload, ensure_ascii=False, indent=2))
        if args.markdown is not None:
            _write_output(args.markdown, templates_markdown(templates))
        return 0

    if args.command == "examples":
        examples = default_example_catalog()
        if args.category is not None:
            examples = [example for example in examples if example.category == args.category]
        payload = examples_records(examples)
        print(examples_markdown(examples))
        if args.json is not None:
            _write_output(args.json, json.dumps(payload, ensure_ascii=False, indent=2))
        if args.markdown is not None:
            _write_output(args.markdown, examples_markdown(examples))
        return 0

    if args.command == "browse":
        portal = default_portal_index()
        payload = portal.records()
        print(portal.to_markdown())
        if args.json is not None:
            _write_output(args.json, json.dumps(payload, ensure_ascii=False, indent=2))
        if args.markdown is not None:
            _write_output(args.markdown, portal.to_markdown())
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
