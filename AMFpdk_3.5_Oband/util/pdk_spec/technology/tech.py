import inspect
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from types import ModuleType
from typing import Tuple

from openpyxl import Workbook

from fnpcell.ansi.term import Color, style
from ..rule import CheckRule
from ..settings import TECHOLOGY_TECH_ATTRS


@dataclass
class TechCheckRule(CheckRule):
    def checked(self, pdk: ModuleType, workbook: Workbook, index: int) -> Tuple[str, str]:
        file_path = Path(__file__).parts[-2:]
        relative_path = pdk.__name__ / Path("/".join(file_path))
        abs_path = [str(pdk.__path__[0] / Path("technology"))]
        load_module_name = ""
        file_path_str = str(relative_path.with_suffix("").as_posix()).replace("/", ".")
        title = f"Checking [{file_path_str}]"
        worksheet = workbook.active
        worksheet.cell(index, 1, f"{file_path_str}").font = self._font  # type: ignore
        self.title = title
        for _, name, _ in iter_modules(abs_path):
            if name == "tech":
                load_module_name = pdk.__name__ + f".technology.{name}"
                break
        else:
            sty = style(color=Color.YELLOW)
            self.style = sty
            return sty, f"[{relative_path}]\n {relative_path.name} not exist(Either provide this file or inherit it from another PDK like GPDK)\n\n"

        try:
            load_module = import_module(load_module_name)
        except Exception as e:
            sty = style(color=Color.RED)
            self.style = sty
            return sty, f"[{relative_path}]\n Failed to import this module(error: {e})\n\n"

        if hasattr(load_module, "TECH") and inspect.isclass(getattr(load_module, "TECH")):
            lack_tech_attrs = [attr for attr in TECHOLOGY_TECH_ATTRS if not hasattr(load_module.TECH, attr)]
            if lack_tech_attrs:
                lack_tech_attrs_ = "\n  ".join(lack_tech_attrs)
                sty = style(color=Color.YELLOW)
                self.style = sty
                return (
                    sty,
                    f"[{file_path_str}]\nThe class TECH lacks attribute(It's better to have {len(TECHOLOGY_TECH_ATTRS)} attributes in the class TECH:{'、'.join(TECHOLOGY_TECH_ATTRS)} for the integrity of PDK):\n  {lack_tech_attrs_}\n\n",
                )
        else:
            sty = style(color=Color.YELLOW)
            self.style = sty
            return (
                sty,
                f"[{file_path_str}]\nClass TECH not in {relative_path.name}(It's better to have class TECH in {relative_path.name} for the integrity of PDK)\n\n",
            )

        return "", ""

    def load_tech(self, pdk: ModuleType):
        abs_path = [str(pdk.__path__[0] / Path("technology"))]
        load_module_name = pdk.__name__ + ".technology."
        for _, name, _ in iter_modules(abs_path):
            if name == "tech":
                load_module_name += name
                break
        else:
            return

        try:
            load_module = import_module(load_module_name)
        except:
            return

        if hasattr(load_module, "TECH") and inspect.isclass(getattr(load_module, "TECH")):
            tech_ = getattr(load_module, "TECH")
            return tech_
        else:
            return
