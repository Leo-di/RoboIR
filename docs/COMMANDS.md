# Commands

RoboIR is designed to be used from a small set of high-signal commands.

## Command matrix

| Command | What it does | Common output |
| --- | --- | --- |
| `roboir run` | execute a task pack with an adapter | report, JSON, markdown |
| `roboir browse` | open the unified portal | markdown portal, JSON index |
| `roboir examples` | browse runnable examples | scenario table, category filters |
| `roboir templates` | list copyable skeletons | template table, JSON export |
| `roboir catalog` | inspect built-in task packs | task pack catalog |
| `roboir adapters` | list adapter backends | adapter catalog |
| `roboir plugins` | discover plugin bundles | plugin index |
| `roboir benchmark` | run a pack benchmark | summary report |
| `roboir suite` | compare multiple packs | suite report |
| `roboir trace` | export trace analysis | trace markdown, JSON |
| `roboir visualize` | render scene or trace diagrams | Mermaid output |
| `roboir report` | produce a structured execution report | markdown / JSON report |
| `roboir scene` | export or load a scene graph | JSON scene file |

## Recommended flow

1. `roboir run --pack deskservice --adapter mock`
2. `roboir browse`
3. `roboir examples`
4. `roboir templates`
5. `roboir benchmark --pack workcell`

## Practical notes

- use `run` for the shortest end-to-end check
- use `browse` to discover the repository structure
- use `examples` when you want runnable scenarios
- use `templates` when you want to build downstream extensions
