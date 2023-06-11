import gpdk
from fnpcell import console
from fnpcell.pdk.technology.all import register_technology

from .tech import TECH as GPDK_TECH
from .wg import WG  # type: ignore

console.info(f"GPDK version: {gpdk.__version__}")
get_technology = register_technology(GPDK_TECH)
