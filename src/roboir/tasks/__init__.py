from .base import TaskPack
from .catalog import TaskCatalog, TaskPackSpec, default_task_catalog
from .deskservice import build_deskservice_pack
from .lab import build_lab_pack
from .office import build_office_pack
from .retail import build_retail_pack
from .workcell import build_workcell_pack

PACK_BUILDERS = {
    "workcell": build_workcell_pack,
    "lab": build_lab_pack,
    "office": build_office_pack,
    "retail": build_retail_pack,
    "deskservice": build_deskservice_pack,
}


def build_task_pack(name: str) -> TaskPack:
    try:
        builder = PACK_BUILDERS[name]
    except KeyError as error:
        available = ", ".join(sorted(PACK_BUILDERS))
        raise ValueError(f"unknown task pack '{name}'. available: {available}") from error
    return builder()


__all__ = [
    "TaskPack",
    "TaskCatalog",
    "TaskPackSpec",
    "default_task_catalog",
    "build_task_pack",
    "build_workcell_pack",
    "build_lab_pack",
    "build_office_pack",
    "build_retail_pack",
    "build_deskservice_pack",
    "PACK_BUILDERS",
]
