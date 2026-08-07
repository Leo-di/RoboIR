from roboir.templates import default_template_catalog


def test_template_catalog_has_three_entries():
    templates = default_template_catalog()
    names = {template.name for template in templates}
    assert names == {"plugin", "adapter", "task_pack"}
