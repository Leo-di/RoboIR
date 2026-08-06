from roboir import GraphNode, GraphRuntime, GraphStatus, RoboIRRuntime, SceneGraph, SceneObject, SkillPlanner, SkillRegistry, StepResult
from roboir.plugins import default_workcell_plugins


def build_runtime() -> RoboIRRuntime:
    registry = SkillRegistry()
    plugin_manager = default_workcell_plugins()
    from roboir import AffordanceMap

    affordance_map = AffordanceMap()
    plugin_manager.install(registry, affordance_map)
    return RoboIRRuntime(graph_runtime=GraphRuntime(skill_registry=registry, affordance_map=affordance_map))


def main() -> None:
    runtime = build_runtime()
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="box_1", label="kit box", category="box"))
    scene.add_object(SceneObject(object_id="item_1", label="screwdriver", category="item"))
    scene.add_object(SceneObject(object_id="tray_1", label="tray", category="tray"))

    planner = SkillPlanner(runtime.graph_runtime.skill_registry)
    best = planner.best(scene, list(runtime.affordance_map.affordances))
    print(f"best_skill={best.skill.name} target={best.scene_object.label}")

    def inspect(_context, memory):
        memory.store("box_state", "opened", source="detect_object")
        return StepResult(GraphStatus.SUCCESS, "box detected")

    def pick(_context, memory):
        memory.store("item_state", "picked", source="grasp_object")
        return StepResult(GraphStatus.SUCCESS, "item picked")

    def place(_context, memory):
        memory.store("tray_state", "loaded", source="place_object")
        return StepResult(GraphStatus.SUCCESS, "item placed")

    plan = [
        GraphNode(name="inspect_box", skill_name="detect_object", action=inspect),
        GraphNode(name="pick_item", skill_name="grasp_object", action=pick),
        GraphNode(name="place_item", skill_name="place_object", action=place),
    ]
    results = runtime.run(goal="kitting", scene_graph=scene, nodes=plan)
    for result in results:
        print(result.status.value, result.message)
    runtime.trace_log.export_json("trace.json")


if __name__ == "__main__":
    main()
