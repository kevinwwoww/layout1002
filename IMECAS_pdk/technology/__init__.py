import IMECAS_pdk
from fnpcell import console
from fnpcell.pdk.technology.all import register_technology

from .tech import TECH as IMECAS_pdk_TECH
from .wg import WG  # type: ignore

console.info(f"IMECAS_pdk version: {IMECAS_pdk.__version__}")
get_technology = register_technology(IMECAS_pdk_TECH)
