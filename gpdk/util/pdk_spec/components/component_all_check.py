import inspect
from collections import abc
from dataclasses import dataclass, is_dataclass, Field
from importlib import import_module
from types import ModuleType
from typing import Tuple, Set, Any, List, Union, Callable

from openpyxl import Workbook

from fnpcell import all as fp
from fnpcell.ansi.term import style, Color
from fnpcell.pdk.pcell_params import PCELL_PARAM
from fnpcell.pdk.technology import all as fpt
from ..rule import CheckRule
from ..settings import NO_NEED_CHECK_MODULES, REQUIRED_ALL_FILES, SDL_SUPPORT_PARAMETER_TYPES, ANNOTATION_TO_DEFAULT_PARAMETER_TYPES_MAP


@dataclass
class ComponentAllCheckRule(CheckRule):
    def checked(self, pdk: ModuleType, workbook: Workbook, index: int) -> Tuple[str, str]:
        all_file_path = pdk.__name__ / REQUIRED_ALL_FILES
        all_file_path_str = str(all_file_path.with_suffix("").as_posix()).replace("/", ".")
        title = f"Checking [{all_file_path_str}]"
        worksheet = workbook.active  # type: ignore
        worksheet.cell(index, 1, f"{all_file_path_str}").font = self._font  # type: ignore
        self.title = title
        all_components_module_vals = {}
        try:
            all_components_module = import_module(all_file_path_str)
            all_components_module_vals = {v: k for k, v in inspect.getmembers(all_components_module, inspect.isclass)}
        except:
            sty = style(color=Color.RED)
            self.style = sty
            return sty, f"[{all_file_path}]\nFailed to import this module(Make sure {all_file_path.name} already exists)\n\n"

        abs_path = pdk.__path__[0] / REQUIRED_ALL_FILES
        all_components_paths = abs_path.parent.rglob("*.py")
        all_components_module_set: Set[Any] = set()
        all_lack_components_module: List[str] = []
        all_incorrect_parameter_types: List[str] = []
        all_sdl_not_suppert_parameter_types: List[str] = []
        call_no_arguments_failed_all_components_module: List[str] = []
        for component_path in all_components_paths:
            if component_path == abs_path:
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
                        incorrect_parameter_types: List[str] = []
                        sdl_not_suppert_parameter_types: List[str] = []
                        cls_val_dataclass_fields = cls_val.__dataclass_fields__ if is_dataclass(cls_val) else {}
                        cls_val_fields = [i for i in cls_val.__dict__ if not i.startswith("__") and not i.endswith("__")]
                        for cls_val_name, cls_val_type in cls_val.__annotations__.items():
                            if cls_val_name in cls_val_fields:
                                cls_val_annotations_type_dict = cls_val_type.__dict__
                                cls_val_annotations_type_origin = cls_val_annotations_type_dict.get("__origin__")
                                cls_val_annotations_type_args = cls_val_annotations_type_dict.get("__args__")
                                cls_val_dataclass_field = cls_val_dataclass_fields.get(cls_val_name)

                                if cls_val_dataclass_field and hasattr(cls_val_dataclass_field, "metadata"):
                                    field_pcell_param = cls_val_dataclass_field.metadata.get(PCELL_PARAM)

                                    match_type = ANNOTATION_TO_DEFAULT_PARAMETER_TYPES_MAP.get(field_pcell_param.__class__)
                                    cls_val_annotations_type_args_no_none = None
                                    if (
                                        match_type
                                        and match_type != cls_val_type
                                        and cls_val_annotations_type_origin == Union
                                        and None.__class__ in cls_val_annotations_type_args
                                    ):
                                        cls_val_annotations_type_args_list = list(cls_val_annotations_type_args)
                                        cls_val_annotations_type_args_list.remove(None.__class__)
                                        if len(cls_val_annotations_type_args_list) == 1:
                                            cls_val_annotations_type_args_no_none = cls_val_annotations_type_args_list[0]

                                    if cls_val_dataclass_field and isinstance(cls_val_dataclass_field, Field):
                                        if (
                                            (match_type and not (match_type == cls_val_type or match_type == cls_val_annotations_type_args_no_none))
                                            or (isinstance(field_pcell_param, type(fp.MappingParam())) and cls_val_annotations_type_origin != abc.Mapping)
                                            or (
                                                isinstance(field_pcell_param, type(fp.WaveguideTypeParam()))
                                                and (inspect.isclass(cls_val_type) and not issubclass(cls_val_type, fpt.IWaveguideType))
                                            )
                                            or (
                                                isinstance(field_pcell_param, type(fp.DeviceParam()))
                                                and (inspect.isclass(cls_val_type) and not issubclass(cls_val_type, fpt.ICellRef))
                                            )
                                        ):
                                            incorrect_parameter_types.append(
                                                f"{cls_val_name} (parameter, annotation type: {cls_val_type}, default type: {field_pcell_param.__class__})"
                                            )
                                        elif not isinstance(field_pcell_param, fp.IParam):
                                            incorrect_parameter_types.append(
                                                f"{cls_val_name} (parameter, the default parameter is not an instance of fp.param)"
                                            )

                                if (
                                    cls_val_type in SDL_SUPPORT_PARAMETER_TYPES
                                    or inspect.isfunction(cls_val_type)
                                    or str(cls_val_type).find("WaveguideType") != -1
                                    or (inspect.isclass(cls_val_type) and issubclass(cls_val_type, fpt.IWaveguideType))
                                ):
                                    continue

                                elif cls_val_annotations_type_origin and cls_val_annotations_type_args:
                                    if cls_val_annotations_type_origin in (list, tuple):
                                        if all(
                                            [
                                                arg.__dict__.get("__origin__") not in (list, tuple, Union, abc.Sequence)
                                                for arg in cls_val_annotations_type_args
                                                if arg != Ellipsis
                                            ]
                                        ):
                                            continue

                                        elif len(cls_val_annotations_type_args) > 0 and cls_val_annotations_type_args[0].__dict__.get("__origin__") == Union:
                                            cls_val_annotations_type_args_ = cls_val_annotations_type_args[0].__dict__.get("__args__")
                                            if all(
                                                [
                                                    arg.__dict__.get("__origin__") not in (list, tuple, Union, abc.Sequence)
                                                    for arg in cls_val_annotations_type_args_
                                                ]
                                            ):
                                                continue

                                    elif cls_val_annotations_type_origin == abc.Sequence:
                                        if all([arg.__dict__.get("__origin__") not in (list, tuple, abc.Sequence) for arg in cls_val_annotations_type_args]):
                                            continue

                                        elif len(cls_val_annotations_type_args) > 0 and cls_val_annotations_type_args[0].__dict__.get("__origin__") in (
                                            tuple,
                                            Union,
                                        ):
                                            cls_val_annotations_type_args_ = cls_val_annotations_type_args[0].__dict__.get("__args__")
                                            if all(
                                                [arg.__dict__.get("__origin__") not in (list, tuple, abc.Sequence) for arg in cls_val_annotations_type_args_]
                                            ):
                                                continue

                                    elif cls_val_annotations_type_origin == abc.Mapping:
                                        continue

                                    elif inspect.isclass(cls_val_annotations_type_origin) and issubclass(cls_val_annotations_type_origin, Callable):
                                        continue

                                sdl_not_suppert_parameter_types.append(f"{cls_val_name} (parameter, type: {cls_val_type})")

                        if incorrect_parameter_types:
                            incorrect_parameter_types_ = "\n    ".join(incorrect_parameter_types)
                            all_incorrect_parameter_types.append(f"{p_str}.{cls_name}:\n    {incorrect_parameter_types_}\n")

                        if sdl_not_suppert_parameter_types:
                            sdl_not_suppert_parameter_types_ = "\n    ".join(sdl_not_suppert_parameter_types)
                            all_sdl_not_suppert_parameter_types.append(f"{p_str}.{cls_name}:\n    {sdl_not_suppert_parameter_types_}\n")

                        if cls_val not in all_components_module_vals:
                            all_lack_components_module.append(f"{p_str}.{cls_name}")

                        library = fp.Library()
                        try:
                            library += cls_val()
                        except:
                            call_no_arguments_failed_all_components_module.append(f"{p_str}.{cls_name}")
                            continue

        if any(
            all_lack_components_module + call_no_arguments_failed_all_components_module + all_sdl_not_suppert_parameter_types + all_incorrect_parameter_types
        ):
            sty = style(color=Color.YELLOW)
            self.style = sty
            all_lack_components_module_ = "\n  ".join(all_lack_components_module)
            result_str = f"[{all_file_path_str}]\n"
            result_str += (
                f"Found components not in {all_file_path.name}(SDL components should be reexported in {all_file_path.name}):\n  {all_lack_components_module_}\n\n"
                if all_lack_components_module
                else ""
            )
            call_no_arguments_failed_all_components_module_ = "\n  ".join(call_no_arguments_failed_all_components_module)
            result_str += (
                f"Found components do not provide default values to all its parameters(SDL components should provide default values to all its paramters, so users can preview them by simply calling them without arguments):\n  {call_no_arguments_failed_all_components_module_}\n\n"
                if call_no_arguments_failed_all_components_module
                else ""
            )
            all_sdl_not_suppert_parameter_types_ = "\n  ".join(all_sdl_not_suppert_parameter_types)
            tip = str(SDL_SUPPORT_PARAMETER_TYPES).strip("[]")
            result_str += (
                f"Found components whose parameter type is not supported by SDL(Please define parameter types according to the following types supported by SDL: {tip}):\n  {all_sdl_not_suppert_parameter_types_}\n"
                if all_sdl_not_suppert_parameter_types_
                else ""
            )
            all_incorrect_parameter_types_ = "\n  ".join(all_incorrect_parameter_types)
            result_str += (
                f"Found components whose annotation parameter type do not match the default parameter type(Please make sure the two parameter types match):\n  {all_incorrect_parameter_types_}\n\n"
                if all_incorrect_parameter_types_
                else ""
            )

            return sty, result_str
        return "", ""
