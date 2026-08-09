# 能力矩阵

RoboIR 的设计目标是作为一个可复用的具身编排层。

## 能力矩阵

| 能力 | 覆盖内容 | 主要入口 |
| --- | --- | --- |
| 编排 | 基于图的规划、验证与恢复 | `roboir run`，`docs/FEATURES.md` |
| 复用 | 技能、可供性、任务包和轨迹 | `roboir templates`，`roboir browse` |
| 执行 | mock、sim、ROS2、Isaac Sim 风格后端 | 适配器 |
| 发现 | 示例、模板、适配器、任务包、插件 | `roboir browse`，`roboir examples` |
| 评估 | 轨迹、报告、基准和套件 | `roboir benchmark`，`roboir suite` |

## 常见流程

- 加载任务包
- 选择适配器
- 执行分阶段图
- 导出轨迹或报告
- 在基准评测中复用同一任务包

## 这意味着什么

好的具身智能框架不只是能跑一个任务。
它还要让任务可复现、可检查、可复用。
