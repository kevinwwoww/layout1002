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
class AutoTransitionCheckRule(TechCheckRule):
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
                f"[{relative_path}]\n tech.py not exist or class TECH not exist in tech.py(Either provide this file or inherit it from another PDK like IMECAS_SiN_pdk_1_0_0)\n\n",
            )
        else:
            if not hasattr(tech_, "AUTO_TRANSITION") or not inspect.isclass(getattr(tech_, "AUTO_TRANSITION")):
                sty = style(color=Color.YELLOW)
                self.style = sty
                return sty, f"[{relative_path}]\n Class TECH has no 'AUTO_TRANSITION' attribute(Please add this attribute for the integrity of PDK)\n\n"

            auto_transition_ = getattr(tech_, "AUTO_TRANSITION")
            if not hasattr(tech_, "WG") or not inspect.isclass(getattr(tech_, "WG")):
                contents.append(f"[{relative_path}]\n Class TECH has no 'WG' attribute(Please add this attribute for the integrity of PDK)")
            else:
                wg_ = getattr(tech_, "WG")
                wg_types = [w_type for w_name, w_type in inspect.getmembers(wg_, inspect.isclass) if w_name != "__class__" and w_name.isupper()]
                if not wg_types:
                    contents.append(f"No classes found in the class WG(It's better to have at least one class in the class WG)")
                else:
                    if hasattr(auto_transition_, "DEFAULT"):
                        if isinstance(auto_transition_.DEFAULT, fpt.AutoTransition):
                            sub_wg_types = [
                                sub_type
                                for w_type in wg_types
                                for sub_name, sub_type in inspect.getmembers(w_type, inspect.isclass)
                                if sub_name != "__class__" and sub_name.isupper()
                            ]
                            if not sub_wg_types:
                                contents.append(
                                    f"No classes found in classes of the class WG(It's better to have at least one class in classes of the class WG)"
                                )
                            else:
                                lack_profile_classes: List[str] = []
                                for sub_wg_type in sub_wg_types:
                                    if not hasattr(sub_wg_type, "profile"):
                                        lack_profile_classes.append(str(sub_wg_type))

                                if lack_profile_classes:
                                    lack_profile_classes_ = "\n  ".join(lack_profile_classes)
                                    contents.append(
                                        f"The classes lack 'profile' attribute in classes of in the class WG(It's better to have 'profile' attribute in classes of the class WG):\n  {lack_profile_classes_}"
                                    )

                                all_transitions: List[Any] = []
                                for w1, w2 in combinations(sub_wg_types, 2):
                                    all_transitions.append(w1 >> w2)

                                all_tapers = [w >> w for w in sub_wg_types]
                                _registry_attr = getattr(auto_transition_.DEFAULT, "_registry")
                                lack_transitions = [
                                    str((t1, t2)) for t1, t2 in all_transitions if _registry_attr.get((t1, t2)) == None and _registry_attr.get((t2, t1)) == None
                                ]
                                lack_tapers = [str(t) for t in all_tapers if _registry_attr.get(t) == None]
                                if lack_transitions:
                                    lack_transitions_ = "\n  ".join(lack_transitions)
                                    contents.append(
                                        f"Found some transitions not in the class WG(It's better to have all transition combinations in namespace(as a class) WG):\n  {lack_transitions_}"
                                    )
                                if lack_tapers:
                                    lack_tapers_ = "\n  ".join(lack_tapers)
                                    contents.append(
                                        f"Found some tapers not in the class WG(It's better to have all taper combinations in namespace(as a class) WG):\n  {lack_tapers_}"
                                    )
                        else:
                            contents.append(
                                f"The type of the return value of the DEFAULT method of the class AUTO_TRANSITION is not expected(It's better to set the return value to an instance of {fpt.AutoTransition})"
                            )
                    else:
                        contents.append(f"Class AUTO_TRANSITION has no 'DEFAULT' attribute(Please add this attribute for the integrity of PDK)\n\n")

        if contents:
            sty = style(color=Color.YELLOW)
            self.style = sty
            contents_ = "\n\n".join(contents)
            return sty, f"[{file_path_str}]\n{contents_}\n\n"

        return "", ""
