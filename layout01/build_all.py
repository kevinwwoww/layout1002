import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from doit.tools import config_changed
from fnpcell import all as fp


def cpu_count():
    try:
        cpu_count = len(os.sched_getaffinity(0))  # type: ignore
    except:
        cpu_count = os.cpu_count()
    return cpu_count or 0


ROOT = Path(__file__).parent

DOIT_CONFIG = {
    "dep_file": str(ROOT / ".doit.db"),
    "num_process": cpu_count(),
    "par_type": "process",
    "check_file_uptodate": "md5",
    "action_string_formatting": "new",
    "failure_verbosity": 0,
    "verbosity": 2,
}

PYTHON_PATH = [
    ROOT.parent,
]
SCRIPT_CIRCUITS = ROOT / "circuits"
BUILD = ROOT / "build"
BUILD_CIRCUITS = BUILD / "circuits"
RESOURCES = (".json", ".gds")
IGNORE = (
    str(SCRIPT_CIRCUITS / "**" / "*.gds"),
    str(SCRIPT_CIRCUITS / "**" / "*.spc"),
)


class RunBuild:
    def __init__(self, build_file: fp.StrPath, target_file: fp.StrPath):
        self.build_file = build_file
        self.target_file = target_file

    def __call__(self):
        subprocess.run(
            [sys.executable, str(self.build_file), str(self.target_file)],
            check=True,
            env={
                **os.environ,
                "PYTHONPATH": os.pathsep.join(str(it) for it in PYTHON_PATH),
            },
        )


def generate_build_tasks():
    pipfreeze = subprocess.run([sys.executable, "-m", "pip", "freeze"], check=True, stdout=subprocess.PIPE, text=True).stdout
    exclude: Set[str] = set()
    for build_file in SCRIPT_CIRCUITS.rglob("build_*.py"):
        sources = tuple(fp.util.collect_deps(PYTHON_PATH, build_file, exclude=exclude).values())
        resources = tuple(r for r in (src.with_suffix(ext) for src in sources for ext in RESOURCES) if r.exists() and not any(r.match(p) for p in IGNORE))
        task_name = build_file.with_suffix("").name
        file_deps = (build_file,) + sources + resources
        target_file = BUILD_CIRCUITS / build_file.with_suffix(".gds").name
        action = RunBuild(build_file=build_file, target_file=target_file)
        yield {
            "basename": task_name,
            "actions": [action],
            "file_dep": file_deps,
            "uptodate": [config_changed(pipfreeze)],
            "targets": [target_file],
        }


def task_build_all():
    yield generate_build_tasks()


def run_tasks(tasks: Dict[str, Any], argv: Optional[List[str]] = None):
    from doit.cmd_base import ModuleTaskLoader
    from doit.doit_cmd import DoitMain

    result = DoitMain(ModuleTaskLoader(tasks)).run(argv or [])  # type: ignore
    if result != 0:
        raise RuntimeError(result)  # type: ignore


def with_config(force_rebuild: bool = False, **items: Any):
    config = {
        **globals(),
        **items,
    }
    config["DOIT_CONFIG"] = {
        **DOIT_CONFIG,
        "always": force_rebuild,
    }
    return config


if __name__ == "__main__":
    run_tasks(with_config(), sys.argv[1:])
