# RoboIR

面向桌面级工业与服务机器人的模块化具身编排层。

RoboIR 把具身智能工作流变成可复用的基础设施：任务包、插件、适配器、轨迹，以及基于图的执行。

## 快速开始

```bash
roboir run --pack deskservice --adapter mock
roboir browse
roboir examples
roboir templates
```

## RoboIR 能提供什么

- **任务包**：封装场景、计划和基准数据
- **插件**：提供可复用技能和可供性
- **适配器**：对接 mock、sim、ROS2、Isaac Sim 等执行面
- **编排**：支持基于图的规划、验证与恢复
- **轨迹**：用于报告、数据集和评估复用

## 典型场景

- 桌面服务编排
- 工业工位整理
- 故障恢复与人工介入
- 可基准化的具身工作流

## 推荐入口

- [`入门`](GETTING_STARTED.md)
- [`能力矩阵`](CAPABILITIES.md)
- [`命令矩阵`](COMMANDS.md)
- [`功能总览`](FEATURES.md)
- [`集成地图`](INTEGRATIONS.md)
- [`使用场景`](USE_CASES.md)
- [`门户`](PORTAL.md)
- [`示例`](EXAMPLES.md)
- [`架构`](ARCHITECTURE.md)
- [`扩展`](EXTENDING.md)

## 最佳阅读顺序

1. [`文档首页`](README.md)
2. [`示例`](EXAMPLES.md)
3. [`能力矩阵`](CAPABILITIES.md)
4. [`命令矩阵`](COMMANDS.md)
5. [`功能总览`](FEATURES.md)

## 仓库导览

- [`README`](../README.md)
- [`文档首页`](README.md)
- [`能力矩阵`](CAPABILITIES.md)
- [`命令矩阵`](COMMANDS.md)
- [`功能总览`](FEATURES.md)
- [`集成地图`](INTEGRATIONS.md)
- [`使用场景`](USE_CASES.md)
- [`门户`](PORTAL.md)
- [`示例`](EXAMPLES.md)
- [`路线图`](ROADMAP.md)

## 为什么要做这个仓库

多数具身智能仓库只围绕模型、基准或单个演示展开。
RoboIR 关注的是把这些部分串起来的基础设施层。
