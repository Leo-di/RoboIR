# 命令矩阵

RoboIR 通过少量高信号命令对外提供能力。

## 命令矩阵

| 命令 | 功能 | 常见输出 |
| --- | --- | --- |
| `roboir run` | 使用适配器执行任务包 | 报告、JSON、Markdown |
| `roboir browse` | 打开统一门户 | 门户 Markdown、JSON 索引 |
| `roboir examples` | 浏览可运行示例 | 场景表、分类过滤 |
| `roboir templates` | 查看可复制骨架 | 模板表、JSON 导出 |
| `roboir catalog` | 查看内置任务包 | 任务包目录 |
| `roboir adapters` | 查看适配器后端 | 适配器目录 |
| `roboir plugins` | 发现插件包 | 插件索引 |
| `roboir benchmark` | 运行任务包基准 | 摘要报告 |
| `roboir suite` | 对比多个任务包 | 套件报告 |
| `roboir trace` | 导出轨迹分析 | 轨迹 Markdown、JSON |
| `roboir visualize` | 渲染场景或轨迹图 | Mermaid 输出 |
| `roboir report` | 生成结构化执行报告 | Markdown / JSON 报告 |
| `roboir scene` | 导出或载入场景图 | JSON 场景文件 |

## 推荐流程

1. `roboir run --pack deskservice --adapter mock`
2. `roboir browse`
3. `roboir examples`
4. `roboir templates`
5. `roboir benchmark --pack workcell`

## 实用提示

- 用 `run` 做最短端到端检查
- 用 `browse` 探索仓库结构
- 用 `examples` 找可运行场景
- 用 `templates` 复制扩展骨架
