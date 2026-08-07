from roboir.discovery import load_plugin_from_module


def test_template_plugin_loads():
    plugin = load_plugin_from_module("roboir_plugins.template")
    assert plugin is not None
    assert plugin.name == "roboir_template_plugin"
