# 任务包模板

这个模板展示了 RoboIR 中最小但有用的任务包表面。

## 任务包应该包含什么

- 场景图
- 计划图
- 基准套件
- 已安装插件的运行时

## 最小模式

```python
from roboir.tasks.template import build_task_pack_template

pack = build_task_pack_template("your_pack_name")
```

## 推荐打包方式

- 保持任务包贴近领域
- 对外暴露一个清晰的构建函数
- 尽量让任务包与插件模块配套
- 加一个基准案例，便于一致比较
