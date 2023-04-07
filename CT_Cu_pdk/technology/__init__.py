import CT_Cu_pdk
from fnpcell import console
from fnpcell.pdk.technology.all import register_technology

from CT_Cu_pdk.technology.tech import TECH as CT_Cu_TECH
from CT_Cu_pdk.technology.wg import WG # type: ignore
from CT_Cu_pdk.technology.pcell import PCell as PCell

console.info(f"CT_Cu_PDK version: {CT_Cu_pdk.__version__}")

get_technology = register_technology(CT_Cu_TECH)
