# RoboIR 示例

RoboIR 示例围绕具身编排、技能路由、恢复和基准流程来组织。

## 快速入口

| 路径 | 展示内容 | 价值 |
| --- | --- | --- |
| `examples/run_deskservice.py` | 桌面服务执行 | 最短的可运行演示路径 |
| `examples/deskservice_orchestration.py` | 图编排 | 展示带恢复的分阶段编排 |
| `examples/workcell_kitting.py` | 工业工位 | 展示技能路由与轨迹导出 |

## 任务导览

### 1. 桌面服务

从最小的端到端流程开始：

- `run_deskservice` — 完整的桌面服务运行
- `deskservice_orchestration` — 带运行时阶段的基于图编排

### 2. 工业工位

进入更结构化的具身工作流：

- `workcell_kitting` — 技能路由与轨迹导出
- `benchmark_workcell` — 同一任务包的基准运行

### 3. 实验室与办公

用基准任务包对比评测路径：

- `benchmark_lab`
- `benchmark_office`

### 4. 恢复

查看故障感知路径：

- `recovery_demo` — 故障与恢复行为

## 场景矩阵

| 场景 | 示例 | 输出风格 |
| --- | --- | --- |
| 桌面服务 | `run_deskservice` | 端到端执行 |
| 图编排 | `deskservice_orchestration` | 分阶段规划 + 验证 |
| 工业工位 | `workcell_kitting` | 技能路由 + 轨迹导出 |
| 恢复 | `recovery_demo` | 故障处理 |
| 基准 | `benchmark_workcell`, `benchmark_lab`, `benchmark_office` | 可重复评测 |

## 完整索引

| 名称 | 分类 | 场景 | 路径 | 说明 |
| --- | --- | --- | --- | --- |
| `run_deskservice` | `execution` | `desk-service execution` | `examples/run_deskservice.py` | 使用适配器完成桌面服务执行 |
| `deskservice_orchestration` | `orchestration` | `graph orchestration` | `examples/deskservice_orchestration.py` | 基于任务帧的规划与运行时执行 |
| `workcell_kitting` | `planning` | `industrial workcell` | `examples/workcell_kitting.py` | 工业工位技能路由与轨迹导出 |
| `recovery_demo` | `recovery` | `failure recovery` | `examples/recovery_demo.py` | 故障与恢复行为 |
| `benchmark_workcell` | `benchmark` | `benchmark suite` | `examples/benchmark_workcell.py` | 工位任务包的基准运行 |
| `benchmark_lab` | `benchmark` | `benchmark suite` | `examples/benchmark_lab.py` | 实验室任务包的基准运行 |
| `benchmark_office` | `benchmark` | `benchmark suite` | `examples/benchmark_office.py` | 办公任务包的基准运行 |

## 推荐顺序

1. `examples/run_deskservice.py`
2. `examples/deskservice_orchestration.py`
3. `examples/workcell_kitting.py`
4. `examples/recovery_demo.py`
5. 基准脚本

## 使用方式

```bash
python examples/run_deskservice.py
roboir examples --category benchmark
```
