import inspect
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import List, Tuple

from openpyxl import Workbook

from fnpcell.ansi.term import Color, style
from fnpcell.pdk.technology.all import Band, BandEnum
from .tech import TechCheckRule
from ..settings import TECH_BANDS_ATTRS


@dataclass
class BandsCheckRule(TechCheckRule):
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
                f"[{relative_path}]\n tech.py not exist or class TECH not exist in tech.py(Either provide this file or inherit it from another PDK like GPDK)\n\n",
            )
        else:
            if not hasattr(tech_, "BAND") or not inspect.isclass(getattr(tech_, "BAND")):
                sty = style(color=Color.YELLOW)
                self.style = sty
                return sty, f"[{relative_path}]\n Class TECH has no 'BAND' attribute(Please add this attribute for the integrity of PDK)\n\n"
            else:
                if not issubclass(getattr(tech_, "BAND"), BandEnum):
                    contents.append(f"The type of the class Band is not expected(It's better to class Band inherit from {BandEnum})")

                lack_tech_attrs: List[str] = []
                incorrect_tech_attrs: List[str] = []
                for attr in TECH_BANDS_ATTRS:
                    if not hasattr(tech_.BAND, attr):
                        lack_tech_attrs.append(attr)
                    elif not isinstance(getattr(tech_.BAND, attr), Band):
                        incorrect_tech_attrs.append(attr)

                if lack_tech_attrs:
                    contents_ = ", ".join(lack_tech_attrs)
                    contents.append(
                        f"Class BAND lacks attribute(It's better to have {len(TECH_BANDS_ATTRS)} attributes in the class Band:{'、'.join(TECH_BANDS_ATTRS)} for the integrity of PDK):\n  {contents_}"
                    )

                if incorrect_tech_attrs:
                    contents_ = ", ".join(incorrect_tech_attrs)
                    contents.append(
                        f"The type of the attribute of the class BAND is not expected(It's better to set the type of attribute of the class BAND to {Band}):{contents_}"
                    )

                if contents:
                    contents_ = "\n\n".join(contents)
                    sty = style(color=Color.YELLOW)
                    self.style = sty
                    return sty, f"[{file_path_str}]\n{contents_}\n\n"

                return "", ""
