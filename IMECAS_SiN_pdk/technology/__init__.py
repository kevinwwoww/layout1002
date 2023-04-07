import IMECAS_SiN_pdk
from fnpcell import console
from fnpcell.pdk.technology.all import register_technology

from .tech import TECH as IMECAS_SiN_pdk_TECH
from .pcell import PCell as PCell
from .wg import WG  # type: ignore

console.info(f"IMECAS_SiN_pdk version: {IMECAS_SiN_pdk.__version__}")
get_technology = register_technology(IMECAS_SiN_pdk_TECH)
