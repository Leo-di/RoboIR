# 入门

这份指南是最快上手 RoboIR 的方式。

## 安装

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .[dev]
```

## 试运行桌面服务任务包

```bash
roboir run --pack deskservice --adapter mock
```

预期输出：

- 终端里会出现一条简洁摘要
- 指定 `--json` 时会输出结构化报告
- 运行时里会保留轨迹、故障和记忆数据

## 其他常用命令

```bash
roboir catalog
roboir benchmark --pack deskservice
roboir suite --packs workcell lab office retail deskservice
roboir plugins
roboir scene --pack deskservice --output scene.json
roboir scene --input scene.json
roboir adapters
roboir report --pack deskservice --json report.json
roboir trace --pack deskservice --markdown trace.md
roboir visualize --pack deskservice --kind scene
roboir visualize --pack deskservice --kind trace
roboir templates
roboir examples
roboir browse
```

## 先扩展什么

如果你想在 RoboIR 上继续做，可以先从下面任一项开始：

- 为新的具身领域增加一个任务包
- 为仿真器或机器人后端增加一个适配器
- 为可复用技能与可供性增加一个插件
