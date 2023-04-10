import inspect
from dataclasses import dataclass
from importlib import import_module
from types import ModuleType
from typing import Tuple, Set, Any, List, Callable

from openpyxl import Workbook

from fnpcell import all as fp
from fnpcell.ansi.term import style, Color
from ..rule import CheckRule
from ..settings import NO_NEED_CHECK_MODULES, REQUIRED_ALL_FILES, REQUIRED_FUNC_ALL_FILES


@dataclass
class ComponentFuncAllCheckRule(CheckRule):
    def checked(self, pdk: ModuleType, workbook: Workbook, index: int) -> Tuple[str, str]:
        all_file_path = pdk.__name__ / REQUIRED_ALL_FILES
        func_all_file_path = pdk.__name__ / REQUIRED_FUNC_ALL_FILES
        all_file_path_str = str(all_file_path.with_suffix("").as_posix()).replace("/", ".")
        func_all_file_path_str = str(func_all_file_path.with_suffix("").as_posix()).replace("/", ".")
        title = f"Checking [{func_all_file_path_str}]"
        worksheet = workbook.active
        worksheet.cell(index, 1, f"{func_all_file_path_str}").font = self._font  # type: ignore
        self.title = title
        fail_import_str: List[str] = []
        all_components_module_vals = {}
        func_all_components_module_vals = {}
        try:
            all_components_module = import_module(all_file_path_str)
            all_components_module_vals = {v: k for k, v in inspect.getmembers(all_components_module, inspect.isclass)}
        except:
            fail_import_str.append(f"{all_file_path_str}")

        try:
            func_all_components_module = import_module(func_all_file_path_str)
            func_all_components_module_vals = {
                k: v for k, v in inspect.getmembers(func_all_components_module, predicate=lambda a: inspect.isfunction(a) or inspect.isclass(a))
            }
        except:
            fail_import_str.append(f"{func_all_file_path_str}")

        if fail_import_str:
            sty = style(color=Color.RED)
            self.style = sty
            return sty, f"[{func_all_file_path}]\nFailed to import this module(Make sure {func_all_file_path.name} already exists)\n\n"

        all_components_module_keys = all_components_module_vals.values()
        abs_path = pdk.__path__[0] / REQUIRED_FUNC_ALL_FILES
        all_components_paths = abs_path.parent.rglob("*.py")
        # all_components_paths = all_file_path.parent.rglob("*.py")
        all_components_module_set: Set[Any] = set()
        func_all_lack_components_module: List[str] = []
        for component_path in all_components_paths:
            if component_path == all_file_path or component_path == func_all_file_path_str:
                continue

            relative_path = pdk.__name__ / component_path.relative_to(pdk.__path__[0])
            p_str = str(relative_path.with_suffix("").as_posix()).replace("/", ".")
            if p_str.find("__init__") == -1 and p_str.find("test_") == -1:
                p_module = import_module(p_str)
                clsmembers = inspect.getmembers(p_module, inspect.isclass)
                for cls_name, cls_val in clsmembers:
                    if cls_val in all_components_module_set:
                        continue
                    else:
                        all_components_module_set.add(cls_val)

                    if issubclass(cls_val, fp.PCell) and cls_name not in NO_NEED_CHECK_MODULES:
                        if cls_val in all_components_module_vals:
                            for cls_val_name, cls_val_type in cls_val.__dict__.items():
                                if not cls_val_name.startswith("_") and not cls_val_name.endswith("_") and isinstance(cls_val_type, Callable):
                                    for k in all_components_module_keys:
                                        if cls_val_type.__str__().find(k) != -1:
                                            break
                                    else:
                                        cls_val_call = getattr(cls_val, cls_val_name)
                                        if inspect.isfunction(cls_val_call):
                                            if cls_val_call.__name__ not in func_all_components_module_vals:
                                                func_all_lack_components_module.append(f"{p_str}.{cls_val_call.__name__}")
                                        else:
                                            if hasattr(cls_val_call, "__class__") and cls_val_call.__class__.__name__ not in func_all_components_module_vals:
                                                func_all_lack_components_module.append(f"{p_str}.{cls_val_call.__class__.__name__}")

        if func_all_lack_components_module:
            sty = style(color=Color.YELLOW)
            self.style = sty
            func_all_lack_components_module_ = "\n  ".join(func_all_lack_components_module)
            result_str = (
                f"\n[{func_all_file_path_str}]\nFound callable objects not in {func_all_file_path.name}(SDL callable objects should be reexported in {func_all_file_path.name}):\n  {func_all_lack_components_module_}\n\n"
                if func_all_lack_components_module
                else ""
            )

            return sty, result_str
        return "", ""
