import inspect
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import List, Tuple

from openpyxl import Workbook

from fnpcell.ansi.term import Color, style
from fnpcell.pdk.technology import all as fpt
from .tech import TechCheckRule


@dataclass
class DisplayCheckRule(TechCheckRule):
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
                f"[{relative_path}]\n tech.py not exist or class TECH not exist in tech.py(Either provide this file or inherit it from another PDK like CT_Al_pdk)\n\n",
            )
        else:
            if not hasattr(tech_, "DISPLAY") or not inspect.isclass(getattr(tech_, "DISPLAY")):
                sty = style(color=Color.YELLOW)
                self.style = sty
                return sty, f"[{relative_path}]\n Class TECH has no 'DISPLAY' attribute(Please add this attribute for the integrity of PDK)\n\n"
            else:
                display_ = getattr(tech_, "DISPLAY")
                if not hasattr(display_, "LAYER_STYLE") or not isinstance(display_.LAYER_STYLE, fpt.LayerStyleSet):
                    contents.append(
                        f"The type of the 'LAYER_STYLE' attribute of the class DISPLAY is not expected(It's better to set the type of the 'LAYER_STYLE' attribute of the class DISPLAY to {fpt.LayerStyleSet})"
                    )

                if contents:
                    contents_ = "\n\n".join(contents)
                    sty = style(color=Color.YELLOW)
                    self.style = sty
                    return sty, f"[{file_path_str}]\n{contents_}\n\n"

                return "", ""
