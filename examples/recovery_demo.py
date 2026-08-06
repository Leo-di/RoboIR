from roboir import Affordance, AffordanceMap, GraphNode, GraphRuntime, GraphStatus, RoboIRRuntime, SceneGraph, SceneObject, SkillRegistry, SkillSpec, StepResult


def build_runtime() -> RoboIRRuntime:
    registry = SkillRegistry()
    registry.register(SkillSpec(name="grasp_object", description="Grasp an object", satisfies=["pick"]))
    affordance_map = AffordanceMap([Affordance(name="grasp_handle", target_category="item", action="pick")])
    return RoboIRRuntime(graph_runtime=GraphRuntime(skill_registry=registry, affordance_map=affordance_map))


def main() -> None:
    runtime = build_runtime()
    scene = SceneGraph()
    scene.add_object(SceneObject(object_id="item_1", label="cup", category="item"))

    def grasp(_context, memory):
        if memory.get("grasp_attempts", 0) == 0:
            memory.store("grasp_attempts", 1, source="grasp_object")
            return StepResult(GraphStatus.FAILED, "grasp failed")
        memory.store("grasp_state", "ok", source="grasp_object")
        return StepResult(GraphStatus.SUCCESS, "grasp succeeded")

    def recover(_context, memory, _result):
        memory.store("grasp_attempts", 1, source="recovery")
        return StepResult(GraphStatus.RECOVERED, "retry after regrasp")

    runtime.recovery_manager.add(recover)
    plan = [GraphNode(name="grasp_item", skill_name="grasp_object", action=grasp)]
    results = runtime.run(goal="pick cup", scene_graph=scene, nodes=plan)
    for result in results:
        print(result.status.value, result.message)
    runtime.trace_log.export_json("recovery_trace.json")


if __name__ == "__main__":
    main()
