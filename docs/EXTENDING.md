# 扩展 RoboIR

`RoboIR` 围绕三个扩展面组织：

1. **插件**——注册可复用技能和可供性
2. **适配器**——对接仿真器或机器人
3. **任务包**——把场景、计划和基准一起打包

可复制的插件骨架见 [`docs/PLUGIN_TEMPLATE.md`](PLUGIN_TEMPLATE.md)。
可复制的任务包骨架见 [`docs/TASK_TEMPLATE.md`](TASK_TEMPLATE.md) 以及 `src/roboir/tasks/template.py`。
可复制的适配器骨架见 [`docs/ADAPTER_TEMPLATE.md`](ADAPTER_TEMPLATE.md) 以及 `src/roboir/adapters/template.py`。

用 `roboir templates` 可以一次查看全部模板。
用 `roboir browse` 可以查看整个仓库的统一门户。

## 插件面

插件需要提供一个 `register()` 方法，并且可以通过入口点发现，或者通过导出 `PLUGIN` / `build_plugin()` 的模块加载。

示例入口点：

```toml
[project.entry-points."roboir.plugins"]
deskservice = "roboir_plugins.deskservice:PLUGIN"
```

## 适配器面

适配器实现 `RobotAdapter` 协议：

- `observe()` 返回机器人侧观察
- `execute(command)` 发送技能命令并返回反馈
- `reset()` 清空适配器状态

`RoboIR` 提供 `mock`、`sim`、`ros2` 和 `isaac_sim` 风格适配器，便于开发和演示。

## 任务包

任务包会绑定：

- 场景图
- 计划图
- 基准套件
- 已安装插件的运行时

`deskservice` 包是仓库里最能代表桌面工业/服务场景的例子。

## 模板模块

`src/roboir_plugins/template.py` 是可以复制到下游仓库的最小插件骨架。

`src/roboir/tasks/template.py` 是可以复制到下游仓库的最小任务包骨架。

`src/roboir/adapters/template.py` 是可以复制到下游仓库的最小适配器骨架。

## 从哪里开始

- 新领域：先复制 `deskservice` 任务包模式
- 新后端：先加适配器，并注册到工厂里
- 新能力：先封装成插件
