import difflib
import inspect
import os
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional

from fnpcell import all as fp


def compare_spice(*, file_a: fp.StrPath, file_b: fp.StrPath, save_diff: bool = False):
    with fp.TextResource(file_a, mode=fp.OpenMode.READ) as f_a:
        lines_a = f_a.readlines()

    with fp.TextResource(file_b, mode=fp.OpenMode.READ) as f_b:
        lines_b = f_b.readlines()

    diff = difflib.unified_diff(lines_a, lines_b, lineterm="")

    for line in diff:
        if line.startswith("-"):
            fp.util.term.print_ansi(fp.util.term.style(color=fp.util.term.Color.GREEN), line)
        elif line.startswith("+"):
            fp.util.term.print_ansi(fp.util.term.style(color=fp.util.term.Color.RED), line)
        else:
            fp.util.term.print_ansi(line)
    if save_diff:
        diff_file = Path(file_a).parent / Path(file_b).name / "_diff.txt"
        with fp.TextResource(diff_file, mode=fp.OpenMode.TRUNCATE) as out:
            out.writelines("\n".join(diff))

    return diff


def compare_spice_with_args(
    *,
    source_file: Optional[fp.StrPath] = None,
    target_file: Optional[fp.StrPath] = None,
    source_folder: str = "_tests",
    delete_temp_spice: bool = True,
    save_diff: bool = False,
    temp_suffix: str = "_temp",
):
    def compare(func: Callable[..., Any]):
        @wraps(func)
        def func_wapper(*args: Any, **kwargs: Any):
            file_name = inspect.getfile(func)
            source_spice_file = source_file
            if source_spice_file is None:
                source_spice_file = Path(file_name).parent.parent / source_folder / Path(file_name).with_suffix(".spc").name.replace("test_", "")
            target_spice_file = target_file
            if target_spice_file is None:
                target_spice_file = (
                    Path(file_name).parent.parent
                    / source_folder
                    / Path(Path(file_name).with_suffix("").name + temp_suffix).with_suffix(".spc").name.replace("test_", "")
                )
            libary = fp.Library()
            libary += func(*args, **kwargs)
            fp.export_spc(libary, file=target_spice_file)

            compare_spice(file_a=source_spice_file, file_b=target_spice_file, save_diff=save_diff)

            if delete_temp_spice:
                os.remove(target_spice_file)

            return func(*args, **kwargs)

        return func_wapper

    return compare


if __name__ == "__main__":
    import os

    cwd = os.getcwd()
    file_0 = Path(cwd).parent / "examples/local/example_sdl_circuit.spc"
    file_1 = Path(cwd).parent / "examples/local/example_sdl_circuit_01.spc"

    result = compare_spice(file_a=file_0, file_b=file_1)
