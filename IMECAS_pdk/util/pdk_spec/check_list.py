from IMECAS_pdk.util.pdk_spec.technology.auto_link import AutoLinkCheckRule
from IMECAS_pdk.util.pdk_spec.technology.auto_transition import AutoTransitionCheckRule
from IMECAS_pdk.util.pdk_spec.technology.auto_vias import AutoViasCheckRule
from IMECAS_pdk.util.pdk_spec.technology.bands import BandsCheckRule
from IMECAS_pdk.util.pdk_spec.technology.display import DisplayCheckRule
from IMECAS_pdk.util.pdk_spec.technology.layers import LayersCheckRule
from IMECAS_pdk.util.pdk_spec.technology.linker import LinkerCheckRule
from IMECAS_pdk.util.pdk_spec.technology.tech import TechCheckRule
from IMECAS_pdk.util.pdk_spec.components.component_all_check import ComponentAllCheckRule
from IMECAS_pdk.util.pdk_spec.components.component_func_all_check import ComponentFuncAllCheckRule
from IMECAS_pdk.util.pdk_spec.components.file_exist_check import FileExistCheckRule

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
