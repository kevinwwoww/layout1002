import inspect
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import List, Tuple

from openpyxl import Workbook

from fnpcell.ansi.term import Color, style
from .tech import TechCheckRule


@dataclass
class LinkerCheckRule(TechCheckRule):
    def checked(self, pdk: ModuleType, workbook: Workbook, index: int) -> Tuple[str, str]:
        contents: List[str] = []
        file_path = Path(__file__).parts[-2:]
        relative_path = pdk.__name__ / Path("/".join(file_path))
        file_path_str = str(relative_path.with_suffix("").as_posix()).replace("/", ".")
        title = f"Checking [{file_path_str}]"
        worksheet = workbook.active
        worksheet.cell(index, 1, f"{file_path_str}").font = self._font  # type: ignore
        self.title = title
        tech_ = self.load_tech(pdk)
        if not tech_:
            sty = style(color=Color.YELLOW)
            self.style = sty
            return (
                sty,
                f"[{relative_path}]\n tech.py not exist or class TECH not exist in tech.py(Either provide this file or inherit it from another PDK like IMECAS_pdk)\n\n",
            )
        else:
            if not hasattr(tech_, "LINKER") or not inspect.isclass(getattr(tech_, "LINKER")):
                sty = style(color=Color.YELLOW)
                self.style = sty
                return sty, f"[{relative_path}]\n Class TECH has no 'LINKER' attribute(Please add this attribute for the integrity of PDK)\n\n"
            else:
                linker_ = getattr(tech_, "LINKER")
                linker_types = [l_type for l_name, l_type in inspect.getmembers(linker_, inspect.isclass) if l_name != "__class__" and l_name.isupper()]
                if not linker_types:
                    contents.append(
                        f"No classes found in the class LINKER(It's better to have class in the class LINKER, it can help reduce the risk of making mistakes)"
                    )

                if contents:
                    sty = style(color=Color.YELLOW)
                    self.style = sty
                    contents_ = "\n\n".join(contents)
                    return sty, f"[{file_path_str}]\n{contents_}\n\n"

                return "", ""
