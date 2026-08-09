# 架构

RoboIR 被组织成一个面向桌面级工业与服务机器人的小型具身编排栈。

设计目标是让框架更像基础设施，而不是一次性演示。

## 数据流

```text
场景 + 任务帧
    ↓
可供性映射
    ↓
技能规划器
    ↓
图运行时
    ↓
具身执行器
    ↓
轨迹 / 故障 / 记忆
```

## 核心层

- `SceneGraph` 保存对象中心状态
- `AffordanceMap` 负责动作机会落地
- `SkillPlanner` 为任务帧排序技能候选
- `GraphRuntime` 执行分阶段图节点
- `EmbodiedExecutor` 将运行逻辑桥接到适配器
- `RecoveryManager` 和 `HumanInTheLoopManager` 处理故障恢复
- `TraceLog` 和 `TraceAnalyzer` 把执行结果转成产物
- `SceneGraph.save_json()` 和 `SceneGraph.load_json()` 让场景状态可迁移
- `default_adapter_catalog()` 暴露支持的后端表面
- `scene_graph_to_mermaid()` 和 `trace_to_mermaid()` 生成轻量图示

## 扩展模型

RoboIR 明确采用插件优先：

- 任务包封装场景、计划和基准
- 插件注册技能和可供性
- 适配器隔离后端执行面
- 报告和数据集都从同一条运行轨迹中生成

## 这带来什么

- 可复用的具身技能库
- 基于图的编排，而不是单次提示
- 面向 mock、仿真和机器人表面的适配器执行
- 可追踪的输出，便于评估和下游复用
