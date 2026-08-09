# 门户

门户是 RoboIR 面向首次访问者的统一入口。

## 为什么重要

高质量的具身智能仓库通常会做好三件事：

- 首页足够短
- 第一条命令足够明确
- 扩展入口足够清晰

RoboIR 用统一门户把这些入口聚合在一起。

## 章节

- 示例 — 运行示例、编排流程和基准
- 模板 — 可复制的扩展骨架
- 适配器 — 支持的执行后端与运行时表面
- 任务包 — 不同具身领域的内置任务包
- 插件 — 可发现的技能与可供性包

## 命令

```bash
roboir browse
roboir browse --section 示例
roboir browse --section 模板
roboir examples
roboir templates
roboir adapters
```

## 推荐路径

1. 运行 `roboir run --pack deskservice --adapter mock`
2. 打开 `roboir browse`
3. 复制一个模板到下游工程
4. 用自己的技能、适配器或任务包继续扩展

## 站点地图

- `docs/README.md`：文档首页
- `docs/HOME.md`：最快阅读路径
- `README.md`：仓库首页
