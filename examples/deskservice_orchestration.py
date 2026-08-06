from roboir import RegionConstraint, TaskFrame, TaskPhase, build_task_pack
from roboir.planner import SkillPlanner
from roboir.policy import RuleBasedPolicy


def main() -> None:
    pack = build_task_pack("deskservice")
    frame = TaskFrame(
        goal="desk assembly handoff",
        pack="deskservice",
        phase=TaskPhase.OBSERVE,
        target_object_ids=("part_1",),
        region_constraints=(RegionConstraint(name="pickup_zone", spatial_hint="table-left"),),
    )
    planner = SkillPlanner(pack.runtime.graph_runtime.skill_registry)
    policy = RuleBasedPolicy(planner)
    decision = policy.decide(pack.scene_graph, pack.runtime.affordance_map, task_frame=frame)
    print(decision)
    report = pack.runtime.run_report(goal=pack.name, scene_graph=pack.scene_graph, nodes=pack.plan, task_frame=frame)
    print(report.summary())
    print(pack.runtime.trace_log.events[0].payload)


if __name__ == "__main__":
    main()
