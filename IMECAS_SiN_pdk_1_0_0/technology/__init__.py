import IMECAS_SiN_pdk_1_0_0
from fnpcell import console
from fnpcell.pdk.technology.all import register_technology

from .tech import TECH as IMECAS_SiN_pdk_1_0_0_TECH
from .pcell import PCell as PCell
from .wg import WG  # type: ignore

console.info(f"IMECAS_SiN_pdk_1_0_0 version: {IMECAS_SiN_pdk_1_0_0.__version__}")
get_technology = register_technology(IMECAS_SiN_pdk_1_0_0_TECH)
