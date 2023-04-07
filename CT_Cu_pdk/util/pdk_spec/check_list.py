from CT_Cu_pdk.util.pdk_spec.technology.auto_link import AutoLinkCheckRule
from CT_Cu_pdk.util.pdk_spec.technology.auto_transition import AutoTransitionCheckRule
from CT_Cu_pdk.util.pdk_spec.technology.auto_vias import AutoViasCheckRule
from CT_Cu_pdk.util.pdk_spec.technology.bands import BandsCheckRule
from CT_Cu_pdk.util.pdk_spec.technology.display import DisplayCheckRule
from CT_Cu_pdk.util.pdk_spec.technology.layers import LayersCheckRule
from CT_Cu_pdk.util.pdk_spec.technology.linker import LinkerCheckRule
from CT_Cu_pdk.util.pdk_spec.technology.tech import TechCheckRule
from CT_Cu_pdk.util.pdk_spec.components.component_all_check import ComponentAllCheckRule
from CT_Cu_pdk.util.pdk_spec.components.component_func_all_check import ComponentFuncAllCheckRule
from CT_Cu_pdk.util.pdk_spec.components.file_exist_check import FileExistCheckRule

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
