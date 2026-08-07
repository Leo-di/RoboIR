from roboir.tasks import build_task_pack_template


def test_task_template_builds():
    pack = build_task_pack_template()
    assert pack.name == "your_pack_name"
    assert pack.scene_graph.summary()["object_count"] == 1
