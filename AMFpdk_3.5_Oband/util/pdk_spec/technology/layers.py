import inspect
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Tuple, List

from openpyxl import Workbook

from fnpcell.ansi.term import Color, style
from fnpcell.pdk.technology.all import LayerEnum, ProcessEnum, PurposeEnum
from .tech import TechCheckRule
from ..settings import TECH_LAYERS_REQUIRED_CLASSES


@dataclass
class LayersCheckRule(TechCheckRule):
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
            lack_classes: List[str] = []
            for cls in TECH_LAYERS_REQUIRED_CLASSES:
                if not hasattr(tech_, cls) or not inspect.isclass(getattr(tech_, cls)):
                    lack_classes.append(cls)

            if len(lack_classes) > 0:
                lack_classes_ = "\n  ".join(lack_classes)
                contents.append(
                    f"""Class TECH lacks attribute(Please make sure class TECH has 'PROCESS' attribute, 'PURPOSE' attribute, and 'LAYER' attribute for the integrity of PDK):\n  {lack_classes_}\n\n"""
                )

            superclsMap = {"PROCESS": ProcessEnum, "PURPOSE": PurposeEnum, "LAYER": LayerEnum}
            exist_classes = [cls for cls in TECH_LAYERS_REQUIRED_CLASSES if cls not in lack_classes]
            for cls in exist_classes:
                supercls = superclsMap[cls]
                if not issubclass(getattr(tech_, cls), supercls):  # type:ignore
                    contents.append(f"The type of the class {cls} is not expected(It's better to class {cls} inherit from {supercls})")

            if contents:
                sty = style(color=Color.YELLOW)
                self.style = sty
                contents_ = "\n\n".join(contents)
                return sty, f"[{file_path_str}]\n{contents_}\n\n"

            return "", ""
