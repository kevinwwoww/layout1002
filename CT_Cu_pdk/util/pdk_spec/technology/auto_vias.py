import inspect
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from types import ModuleType
from typing import Any, List, Tuple

from openpyxl import Workbook

from fnpcell.ansi.term import Color, style
from fnpcell.pdk.technology import all as fpt
from .tech import TechCheckRule


@dataclass
class AutoViasCheckRule(TechCheckRule):
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
                f"[{relative_path}]\n tech.py not exist or class TECH not exist in tech.py(Either provide this file or inherit it from another PDK like CT_Cu_pdk)\n\n",
            )
        else:
            if not hasattr(tech_, "AUTO_VIAS") or not inspect.isclass(getattr(tech_, "AUTO_VIAS")):
                sty = style(color=Color.YELLOW)
                self.style = sty
                return sty, f"[{relative_path}]\n Class TECH has no 'AUTO_VIAS' attribute(Please add this attribute for the integrity of PDK)\n\n"

            auto_vias_ = getattr(tech_, "AUTO_VIAS")
            if not hasattr(tech_, "METAL") or not inspect.isclass(getattr(tech_, "METAL")):
                contents.append(f"[{relative_path}]\n Class TECH has no 'METAL' attribute(Please add this attribute for the integrity of PDK)")
            else:
                metal_ = getattr(tech_, "METAL")
                metal_methods = [m_name for m_name, _ in inspect.getmembers(metal_) if m_name != "__class__"]
                if "metal_stack" not in metal_methods or "from_single_layer" not in metal_methods:
                    contents.append(
                        f"The metal_stack method or from_single_layer method is missing in the class METAL(It's better to have metal_stack method and from_single_layer method in the class METAL)"
                    )

                metal_types = [m_type for m_name, m_type in inspect.getmembers(metal_, inspect.isclass) if m_name != "__class__" and m_name.isupper()]
                if not metal_types:
                    contents.append(f"No classes found in the class METAL(It's better to have at least one class in the class METAL)")
                else:
                    if hasattr(auto_vias_, "DEFAULT"):
                        if isinstance(auto_vias_.DEFAULT, fpt.AutoVias):
                            lack_profile_classes: List[str] = []
                            for metal_type in metal_types:
                                if not hasattr(metal_type, "profile"):
                                    lack_profile_classes.append(str(metal_type))

                            if lack_profile_classes:
                                lack_profile_classes_ = "\n  ".join(lack_profile_classes)
                                contents.append(
                                    f"The classes lack 'profile' attribute in the class METAL(It's better to have 'profile' attribute of the classes in the class METAL):\n  {lack_profile_classes_}"
                                )

                            all_transitions: List[Any] = []
                            for w1, w2 in combinations(metal_types, 2):
                                all_transitions.append(w1 >> w2)

                            all_tapers = [w >> w for w in metal_types]
                            _registry_attr = getattr(auto_vias_.DEFAULT, "_registry")
                            lack_transitions = [
                                str((t1, t2)) for t1, t2 in all_transitions if _registry_attr.get((t1, t2)) == None and _registry_attr.get((t2, t1)) == None
                            ]
                            lack_tapers = [str(t) for t in all_tapers if _registry_attr.get(t) == None]
                            if len(lack_transitions) > 0:
                                lack_transitions_ = "\n  ".join(lack_transitions)
                                contents.append(
                                    f"Found some viases not in the class METAL(It's better to have all vias combinations in namespace(as a class) METAL):\n  {lack_transitions_}"
                                )
                            if len(lack_tapers) > 0:
                                lack_tapers_ = "\n  ".join(lack_tapers)
                                contents.append(
                                    f"Found some tapers not in the class METAL(It's better to have all taper combinations in namespace(as a class) METAL):\n  {lack_tapers_}"
                                )
                        else:
                            contents.append(
                                f"The type of the return value of the DEFAULT method of the class AUTO_VIAS is not expected(It's better to set the return value to an instance of {fpt.AutoVias})"
                            )
                    else:
                        contents.append(f"Class AUTO_VIAS has no 'DEFAULT' attribute(Please add this attribute for the integrity of PDK)\n\n")

            if contents:
                sty = style(color=Color.YELLOW)
                self.style = sty
                contents_ = "\n\n".join(contents)
                return sty, f"[{file_path_str}]\n{contents_}\n\n"

            return "", ""
