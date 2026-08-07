from roboir.adapters.factory import build_robot_adapter
from roboir.embodied import TaskFrame, TaskPhase
from roboir.executor import EmbodiedExecutor
from roboir.tasks import build_task_pack


def main() -> None:
    pack = build_task_pack("deskservice")
    adapter = build_robot_adapter("mock")
    frame = TaskFrame(goal=pack.name, pack=pack.name, phase=TaskPhase.OBSERVE)
    executor = EmbodiedExecutor(runtime=pack.runtime, adapter=adapter)
    results = executor.run(goal=pack.name, scene_graph=pack.scene_graph, nodes=pack.plan, task_frame=frame)
    for result in results:
        print(result.status.value, result.message)


if __name__ == "__main__":
    main()
