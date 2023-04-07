from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.util import all as util

from layout01.build_all import BUILD, BUILD_CIRCUITS, run_tasks, with_config

TARGET_LAYOUT_01 = BUILD / "layout01.gds"

GDS_FILES = {
    "circuit_01": BUILD_CIRCUITS / "build_circuit_01.gds",
    "circuit_02": BUILD_CIRCUITS / "build_circuit_02.gds",
    "circuit_04": BUILD_CIRCUITS / "build_circuit_04.gds",
}


def run_combine_builds():
    # =============================================================
    cell = util.combine_builds(
        "layout01",
        [
            {
                "label": "CIRCUIT01",
                "designer": "Y",
                "source": fp.import_from_gds(file=GDS_FILES["circuit_01"]),
                "description": "circuit 01 for demo",
                "origin": (0, 0),
                "dimensions": (2000, 600),
            },
            {
                "label": "CIRCUIT02",
                "designer": "C",
                "source": fp.import_from_gds(file=GDS_FILES["circuit_02"]),
                "description": "circuit 02 for demo",
                "origin": (0, 600),
                "dimensions": (2000, 600),
            },
            {
                "label": "CIRCUITNN",
                "designer": "B",
                "source": fp.import_from_gds(file=GDS_FILES["circuit_04"]),
                "description": "circuit NN for demo",
                "origin": (2000, 600),
                "dimensions": (2000, 600),
            },
            {
                "label": "CIRCUITMM",
                "designer": "A",
                "source": pdk.Via(),
                "description": "circuit MM for demo",
                "origin": (2000, 0),
                "dimensions": (2000, 600),
            },
            {
                "label": "CIRCUITKK",
                "designer": "A",
                "source": None,
                "description": "circuit MM for demo",
                "origin": (0, -600),
                "dimensions": (2000, 600),
            },
            {
                "label": "CIRCUITJJ",
                "designer": "A",
                "source": None,
                "description": "circuit MM for demo",
                "origin": (2000, -600),
                "dimensions": (2000, 600),
            },
        ],
    )
    # =============================================================
    fp.export_gds(cell, file=TARGET_LAYOUT_01)


def task_combine_builds():
    return {
        "actions": [run_combine_builds],
        "file_dep": [
            *GDS_FILES.values(),
        ],
        "targets": [TARGET_LAYOUT_01],
    }


if __name__ == "__main__":
    import sys

    run_tasks(
        with_config(
            # force_rebuild=True,
            **globals(),
        ),
        sys.argv[1:],
    )
