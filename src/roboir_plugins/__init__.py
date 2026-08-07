from .deskservice import PLUGIN as DESKSERVICE_PLUGIN, build_plugin as build_deskservice_plugin
from .template import PLUGIN as TEMPLATE_PLUGIN, build_plugin as build_template_plugin

PLUGIN = DESKSERVICE_PLUGIN
build_plugin = build_deskservice_plugin

__all__ = [
    "PLUGIN",
    "build_plugin",
    "DESKSERVICE_PLUGIN",
    "build_deskservice_plugin",
    "TEMPLATE_PLUGIN",
    "build_template_plugin",
]
