# RoboIR

RoboIR 是一个面向桌面级工业与服务机器人任务的模块化具身编排层。

它把感知、VLA 策略、规划、执行、恢复、记忆和人工介入连接成一套可复用的基础设施。

[![CI](https://github.com/Leo-di/RoboIR/actions/workflows/ci.yml/badge.svg)](https://github.com/Leo-di/RoboIR/actions/workflows/ci.yml)
[![Issues](https://img.shields.io/github/issues/Leo-di/RoboIR)](https://github.com/Leo-di/RoboIR/issues)
[![PRs](https://img.shields.io/github/issues-pr/Leo-di/RoboIR)](https://github.com/Leo-di/RoboIR/pulls)
[![License](https://img.shields.io/github/license/Leo-di/RoboIR)](./LICENSE)

## 为什么要做这个仓库

多数具身智能仓库只解决模型、基准或者单个演示。
RoboIR 关注的是缺失的基础设施层：

- 技能与可供性复用
- 基于图的编排
- 基于适配器的执行
- 轨迹、基准和数据集导出
- 以插件为中心的扩展方式

## 先试什么

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .[dev]
roboir run --pack deskservice --adapter mock
roboir browse
roboir examples
roboir templates
```

## 重点场景

- 桌面服务编排
- 工业工位整理
- 故障恢复与验证
- 可基准化的具身任务包

## 主要入口

- `roboir run` — 使用适配器执行任务包
- `roboir browse` — 统一浏览示例、模板、适配器、任务包和插件
- `roboir examples` — 可筛选的示例索引
- `roboir templates` — 可复制的扩展骨架
- `roboir catalog` — 内置任务包目录
- `roboir plugins` — 已发现插件目录
- `roboir benchmark` — 单任务包基准运行
- `roboir suite` — 多任务包评测

## 入口视图

`roboir browse --section Examples --section Templates`

这样仓库更像一个真正可浏览的框架首页，而不是论文代码堆。

## 扩展方式

- 任务包封装场景、计划和基准状态
- 插件提供可复用技能与可供性
- 适配器隔离后端执行面
- 轨迹可以进一步生成报告、数据集和可视化

## 仓库结构

```text
src/roboir/
  cli.py
  portal.py
  examples.py
  templates.py
  tasks/
  adapters/
  graph.py
  runtime.py
  executor.py
  trace.py
  report.py
examples/
docs/
```

## 场景示例

- `examples/run_deskservice.py` — 使用 mock 适配器的桌面服务执行
- `examples/deskservice_orchestration.py` — 基于图的编排流程
- `examples/workcell_kitting.py` — 工业技能路由与轨迹导出
- `examples/recovery_demo.py` — 故障恢复与人工介入演示
- `examples/benchmark_workcell.py` — 工位基准运行

## 文档

- `mkdocs.yml`
- `docs/index.md`
- `docs/README.md`
- `docs/HOME.md`
- `docs/GETTING_STARTED.md`
- `docs/ARCHITECTURE.md`
- `docs/CAPABILITIES.md`
- `docs/COMMANDS.md`
- `docs/PORTAL.md`
- `docs/FEATURES.md`
- `docs/INTEGRATIONS.md`
- `docs/USE_CASES.md`
- `docs/EXTENDING.md`
- `docs/ROADMAP.md`

## 方向

RoboIR 希望成为具身智能的编排与复用层，目标更接近一个基础设施仓库，而不是单一机器人策略实现。
