# 插件模板

这个模板展示了 RoboIR 中最小但有用的插件表面。

## 插件应该提供什么

- 一个 `PLUGIN` 对象
- 一个 `build_plugin()` 函数
- 一个或多个可复用的 `SkillSpec`
- 一个或多个匹配的 `Affordance`

## 最小模式

```python
from roboir import Affordance, StaticPlugin, SkillSpec, TaskPhase


PLUGIN = StaticPlugin(
    name="your_plugin_name",
    skills=(
        SkillSpec(
            name="your_skill_name",
            description="在这里描述可复用技能",
            satisfies=["inspect"],
            supported_phases=(TaskPhase.OBSERVE.value,),
        ),
    ),
    affordances=(
        Affordance(
            name="your_affordance_name",
            target_category="item",
            action="inspect",
        ),
    ),
)


def build_plugin() -> StaticPlugin:
    return PLUGIN
```

## 推荐打包方式

- 把插件放在 `src/` 下的小模块里
- 如果要自动发现，就通过 `roboir.plugins` 暴露它
- 命名尽量贴近领域，不要过于泛化
