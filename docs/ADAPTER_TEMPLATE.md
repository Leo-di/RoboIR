# 适配器模板

这个模板展示了 RoboIR 中最小但有用的适配器表面。

## 适配器应该提供什么

- 一个 `name` 字段
- `observe()` 用于机器人侧状态
- `execute(command)` 用于后端执行
- `reset()` 用于重新开始

## 最小模式

```python
from roboir.adapters.template import TemplateRobotAdapter

adapter = TemplateRobotAdapter()
```

## 推荐打包方式

- 保持适配器与后端绑定
- 把外部系统调用映射成 `RobotCommand` 和 `RobotFeedback`
- 不要让适配器承担领域规划逻辑
