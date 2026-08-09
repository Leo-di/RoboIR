from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adapters.factory import build_robot_adapter
from .adapters.catalog import default_adapter_catalog
from .analysis import TraceAnalyzer
from .discovery import discover_entry_point_plugins
from .embodied import TaskFrame, TaskPhase
from .examples import default_example_catalog, examples_markdown, examples_records
from .executor import EmbodiedExecutor
from .portal import default_portal_index, portal_sections
from .report import ExecutionReport
from .scene import SceneGraph
from .suite import TaskSuite
from .tasks import PACK_BUILDERS, build_task_pack, default_task_catalog
from .templates import default_template_catalog, templates_markdown, templates_records
from .visualization import scene_graph_to_mermaid, trace_to_mermaid


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="roboir", description="RoboIR 命令行接口")
    subparsers = parser.add_subparsers(dest="command", required=True)

    task_choices = sorted(PACK_BUILDERS)

    demo_parser = subparsers.add_parser("demo", help="运行任务包演示")
    demo_parser.add_argument("--pack", choices=task_choices, default="workcell")
    demo_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 报告输出")

    benchmark_parser = subparsers.add_parser("benchmark", help="运行任务包基准")
    benchmark_parser.add_argument("--pack", choices=task_choices, default="workcell")
    benchmark_parser.add_argument("--json", type=Path, default=None, help="可选的 JSON 摘要输出路径")
    benchmark_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 摘要输出")

    run_parser = subparsers.add_parser("run", help="使用适配器运行任务包")
    run_parser.add_argument("--pack", choices=task_choices, default="deskservice")
    run_parser.add_argument("--adapter", choices=["mock", "sim", "ros2", "isaac_sim"], default="mock")
    run_parser.add_argument("--json", type=Path, default=None, help="可选的 JSON 报告输出路径")
    run_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 报告输出")

    suite_parser = subparsers.add_parser("suite", help="运行多个任务包的基准套件")
    suite_parser.add_argument("--packs", nargs="+", choices=task_choices, default=task_choices)
    suite_parser.add_argument("--json", type=Path, default=None, help="可选的 JSON 摘要输出路径")
    suite_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 摘要输出")

    export_parser = subparsers.add_parser("export", help="从任务包演示导出轨迹数据集")
    export_parser.add_argument("--pack", choices=task_choices, default="workcell")
    export_parser.add_argument("--output", type=Path, default=Path("trace.jsonl"), help="输出 JSONL 路径")
    export_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 报告输出")

    analyze_parser = subparsers.add_parser("analyze", help="分析轨迹数据集")
    analyze_parser.add_argument("--input", type=Path, required=True, help="输入 JSONL 轨迹数据集")
    analyze_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 报告输出")

    catalog_parser = subparsers.add_parser("catalog", help="查看可用任务包")
    catalog_parser.add_argument("--json", type=Path, default=None, help="可选的 JSON 输出路径")
    catalog_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 输出")

    plugins_parser = subparsers.add_parser("plugins", help="查看已发现插件")
    plugins_parser.add_argument("--json", type=Path, default=None, help="可选的 JSON 输出路径")
    plugins_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 输出")

    scene_parser = subparsers.add_parser("scene", help="导出或查看场景图")
    scene_parser.add_argument("--pack", choices=task_choices, default="deskservice")
    scene_parser.add_argument("--output", type=Path, default=None, help="可选的 JSON 场景输出路径")
    scene_parser.add_argument("--input", type=Path, default=None, help="可选的 JSON 场景输入路径")
    scene_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 输出")

    adapters_parser = subparsers.add_parser("adapters", help="查看可用适配器后端")
    adapters_parser.add_argument("--json", type=Path, default=None, help="可选的 JSON 输出路径")
    adapters_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 输出")

    templates_parser = subparsers.add_parser("templates", help="查看可复制模板模块")
    templates_parser.add_argument("--json", type=Path, default=None, help="可选的 JSON 输出路径")
    templates_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 输出")

    examples_parser = subparsers.add_parser("examples", help="查看精选示例")
    examples_parser.add_argument("--category", choices=sorted({example.category for example in default_example_catalog()}), default=None, help="可选的分类过滤")
    examples_parser.add_argument("--json", type=Path, default=None, help="可选的 JSON 输出路径")
    examples_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 输出")

    browse_parser = subparsers.add_parser("browse", help="浏览统一门户")
    browse_parser.add_argument("--section", choices=portal_sections(), action="append", default=None, help="可选的章节过滤，可重复指定")
    browse_parser.add_argument("--json", type=Path, default=None, help="可选的 JSON 输出路径")
    browse_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 输出")

    report_parser = subparsers.add_parser("report", help="运行任务包并导出报告")
    report_parser.add_argument("--pack", choices=task_choices, default="deskservice")
    report_parser.add_argument("--json", type=Path, default=None, help="可选的 JSON 报告输出路径")
    report_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 报告输出")

    trace_parser = subparsers.add_parser("trace", help="运行任务包并导出轨迹")
    trace_parser.add_argument("--pack", choices=task_choices, default="deskservice")
    trace_parser.add_argument("--json", type=Path, default=None, help="可选的 JSON 轨迹输出路径")
    trace_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 轨迹输出")

    visualize_parser = subparsers.add_parser("visualize", help="将场景或轨迹渲染为 Mermaid")
    visualize_parser.add_argument("--pack", choices=task_choices, default="deskservice")
    visualize_parser.add_argument("--kind", choices=["scene", "trace"], default="scene")
    visualize_parser.add_argument("--output", type=Path, default=None, help="可选的 Mermaid 输出路径")
    visualize_parser.add_argument("--markdown", type=Path, default=None, help="可选的 Markdown 输出")

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
            f"运行完成：任务包={pack.name} 适配器={args.adapter} "
            f"步骤数={report.summary()['result_count']} "
            f"成功={report.success_count} 失败={report.failure_count}"
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
        print(f"已导出数据集到 {args.output}")
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
            lines = ["# 已发现插件", ""]
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
            lines = ["# 场景图", ""]
            summary = payload["summary"]
            lines.extend(
                [
                    f"- 对象数：{summary['object_count']}",
                    f"- 关系数：{summary['relation_count']}",
                    f"- 分类：{', '.join(summary['categories']) if summary['categories'] else '无'}",
                    "",
                    "## 对象",
                ]
            )
            for item in payload["objects"]:
                lines.append(f"- `{item['object_id']}` — {item['label']}（{item['category']}）")
            lines.extend(["", "## 关系"])
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
            lines = ["# 适配器目录", ""]
            for adapter in adapters:
                lines.append(f"- `{adapter.name}` — {adapter.kind}：{adapter.description}")
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
            mermaid = scene_graph_to_mermaid(pack.scene_graph, title=f"{pack.name} 场景")
        else:
            pack.runtime.run(goal=pack.name, scene_graph=pack.scene_graph, nodes=pack.plan)
            mermaid = trace_to_mermaid(pack.runtime.trace_log, title=f"{pack.name} 轨迹")
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
        if args.section is not None:
            portal = portal.with_sections(set(args.section))
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
