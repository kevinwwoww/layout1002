import shutil
from dataclasses import dataclass
from importlib.metadata import version
from typing import List, Tuple, Union
from pkg_resources import parse_version

from fnpcell.ansi.term import Color, print_ansi, style


@dataclass(frozen=True)
class Strict:
    version: str


def check_requirements(**requirements: Union[str, Strict]):
    terminal_width = shutil.get_terminal_size().columns
    print_ansi(" Checking requirements ".center(terminal_width, "="))

    failed_requirements: List[Tuple[str, str]] = []
    total_count = len(requirements)
    for i, (name, required_version) in enumerate(requirements.items()):
        current_version = _distribution_version(name)
        if isinstance(required_version, Strict):
            prefix = f"Checking [{name} == {required_version.version}]"
            success = current_version == required_version.version
        else:
            prefix = f"Checking [{name} >= {required_version}]"
            success = parse_version(current_version) >= parse_version(required_version)

        progress = f"{round((i + 1) / total_count * 100)}%"
        progress = f"[{progress.rjust(4)}]".rjust(terminal_width - len(prefix))

        if success:
            print_ansi(prefix, style(color=Color.GREEN), progress)
        else:
            failed_requirements.append((name, current_version))
            print_ansi(prefix, style(color=Color.RED), progress)
    if not failed_requirements:
        print_ansi(style(color=Color.GREEN), " PASSED ".center(terminal_width, "="))
        print_ansi(style(color=Color.GREEN), "Requirements are all satisfied.")
    else:
        print_ansi(style(color=Color.RED), " FAILED ".center(terminal_width, "="))
        for name, current_version in failed_requirements:
            required_version = requirements[name]
            print_ansi(style(color=Color.RED), f"{name} => {current_version}, requires {required_version}")

    return failed_requirements


def _distribution_version(name: str):
    if name == "fnpcell":
        import fnpcell

        return fnpcell.__version__
    elif name == "CT_Cu_pdk":
        import CT_Cu_pdk

        return CT_Cu_pdk.__version__

    try:
        return version(name)
    except:
        return "0.0.0.dev"
