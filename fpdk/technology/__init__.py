import fpdk
from fnpcell import console
from fnpcell.pdk.technology.all import register_technology

from .tech import TECH as FPDK_TECH
from .wg import WG  # type: ignore

console.info(f"FPDK version: {fpdk.__version__}")
get_technology = register_technology(FPDK_TECH)
