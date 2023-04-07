import CT_pCu_pdk
from fnpcell import console
from fnpcell.pdk.technology.all import register_technology

from CT_pCu_pdk.technology.tech import TECH as CT_Cu_TECH
from CT_pCu_pdk.technology.wg import WG # type: ignore
from CT_pCu_pdk.technology.pcell import PCell as PCell

console.info(f"CT_Cu_PDK version: {CT_pCu_pdk.__version__}")

get_technology = register_technology(CT_Cu_TECH)
