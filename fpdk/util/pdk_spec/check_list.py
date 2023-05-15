from fpdk.util.pdk_spec.technology.auto_link import AutoLinkCheckRule
from fpdk.util.pdk_spec.technology.auto_transition import AutoTransitionCheckRule
from fpdk.util.pdk_spec.technology.auto_vias import AutoViasCheckRule
from fpdk.util.pdk_spec.technology.bands import BandsCheckRule
from fpdk.util.pdk_spec.technology.display import DisplayCheckRule
from fpdk.util.pdk_spec.technology.layers import LayersCheckRule
from fpdk.util.pdk_spec.technology.linker import LinkerCheckRule
from fpdk.util.pdk_spec.technology.tech import TechCheckRule
from fpdk.util.pdk_spec.components.component_all_check import ComponentAllCheckRule
from fpdk.util.pdk_spec.components.component_func_all_check import ComponentFuncAllCheckRule
from fpdk.util.pdk_spec.components.file_exist_check import FileExistCheckRule

BASIC_RULES = [
    AutoLinkCheckRule(),
    AutoTransitionCheckRule(),
    AutoViasCheckRule(),
    BandsCheckRule(),
    DisplayCheckRule(),
    LayersCheckRule(),
    LinkerCheckRule(),
    TechCheckRule(),
    ComponentAllCheckRule(),
    FileExistCheckRule(),
]

EXTEND_RULES = [
    ComponentFuncAllCheckRule(),
]
