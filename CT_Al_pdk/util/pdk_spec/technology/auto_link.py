import inspect
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, List, Mapping, Tuple

from openpyxl import Workbook

from fnpcell.ansi.term import Color, style
from fnpcell.pdk.technology import all as fpt
from .tech import TechCheckRule


@dataclass
class AutoLinkCheckRule(TechCheckRule):
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
            if not hasattr(tech_, "LINKING_POLICY") or not inspect.isclass(getattr(tech_, "LINKING_POLICY")):
                sty = style(color=Color.YELLOW)
                self.style = sty
                return sty, f"[{relative_path}]\n Class TECH has no 'LINKING_POLICY' attribute(Please add this attribute for the integrity of PDK)\n\n"

            linking_policy_ = getattr(tech_, "LINKING_POLICY")
            if not hasattr(tech_, "WG") or not inspect.isclass(getattr(tech_, "WG")):
                contents.append(f"[{relative_path}]\n Class TECH has no 'WG' attribute(Please add this attribute for the integrity of PDK)")
            else:
                wg_ = getattr(tech_, "WG")
                wg_types = [w_type for w_name, w_type in inspect.getmembers(wg_, inspect.isclass) if w_name != "__class__" and w_name.isupper()]
                if not wg_types:
                    contents.append(f"No classes found in the class WG(It's better to have at least one class in the class WG)")
                else:
                    if hasattr(linking_policy_, "DEFAULT"):
                        if isinstance(linking_policy_.DEFAULT, fpt.LinkingPolicy):
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
                                auto_link_types: Mapping[Any, str] = {}
                                for sub_wg_type in sub_wg_types:
                                    if not hasattr(sub_wg_type, "profile"):
                                        lack_profile_classes.append(str(sub_wg_type))

                                    for sub_w_name, sub_w_type in inspect.getmembers(sub_wg_type):
                                        if sub_w_name.isupper() and not inspect.isclass(sub_w_type):
                                            auto_link_types[sub_w_type.__class__] = f"{sub_wg_type}.{sub_w_name}"

                                if lack_profile_classes:
                                    lack_profile_classes_ = "\n  ".join(lack_profile_classes)
                                    contents.append(
                                        f"Found classes lack 'profile' attribute in the class WG(It's better to have 'profile' attribute of classes in the class WG):\n  {lack_profile_classes_}"
                                    )

                                all_auto_links: Mapping[Any, Any] = {}
                                for w1, w2 in combinations(auto_link_types, 2):
                                    all_auto_links[w1 >> w2] = (auto_link_types[w1], auto_link_types[w2])

                                all_auto_links.update({w >> w: (auto_link_types[w], auto_link_types[w]) for w in auto_link_types})
                                _registry_attr = getattr(linking_policy_.DEFAULT, "_registry")
                                lack_auto_links: List[str] = []
                                abnormal_link_and_bend: List[str] = []
                                for k, v in all_auto_links.items():
                                    k1, k2 = k
                                    link_and_bend = _registry_attr.get((k1, k2)) if _registry_attr.get((k1, k2)) else _registry_attr.get((k2, k1))
                                    if link_and_bend:
                                        link_prefer, bend_using = link_and_bend
                                        link_prefer_class = link_prefer.__class__
                                        bend_using_class = bend_using.__class__
                                        if (
                                            not isinstance(link_prefer, Callable)
                                            or link_prefer_class(fpt.IWaveguideType)([fpt.IWaveguideType, fpt.IWaveguideType]) != fpt.IWaveguideType
                                        ):
                                            abnormal_link_and_bend.append(link_prefer_class)

                                        if (
                                            not isinstance(bend_using, Callable)
                                            or bend_using_class(fpt.IBendWaveguideFactory)([fpt.IWaveguideType, fpt.IWaveguideType])
                                            != fpt.IBendWaveguideFactory
                                        ):
                                            abnormal_link_and_bend.append(bend_using_class)

                                    else:
                                        lack_auto_links.append(str(v))

                                if lack_auto_links:
                                    lack_auto_links_ = "\n  ".join(lack_auto_links)
                                    contents.append(
                                        f"Found some link specs not in the class WG(It's better to have all link spec combinations in namespace(as a class) WG):\n  {lack_auto_links_}"
                                    )

                                if abnormal_link_and_bend:
                                    abnormal_link_and_bend_ = [
                                        f"The definition or return value of {i} is not expected(It's better to make an instance of the class callable, with the return value set to an instance of the class)"
                                        for i in set(abnormal_link_and_bend)
                                    ]
                                    abnormal_link_and_bend_ = "\n\n".join(abnormal_link_and_bend_)
                                    contents.append(abnormal_link_and_bend_)
                        else:
                            contents.append(
                                f"The type of the return value of the DEFAULT method of the class LINKING_POLICY is not expected(It's better to set the return value to an instance of {fpt.LinkingPolicy})"
                            )
                    else:
                        contents.append(f"Class LINKING_POLICY has no 'DEFAULT' attribute(Please add this attribute for the integrity of PDK)")

        if contents:
            sty = style(color=Color.YELLOW)
            self.style = sty
            contents_ = "\n\n".join(contents)
            return sty, f"[{file_path_str}]\n{contents_}\n\n"

        return "", ""
