import SITRI_pdk
from fnpcell import console
from fnpcell.pdk.technology.all import register_technology

from SITRI_pdk.technology.tech import TECH as AMF_TECH
from SITRI_pdk.technology.wg import WG # type: ignore

console.info(f"SITRI_pdk version: {SITRI_pdk.__version__}")

get_technology = register_technology(AMF_TECH)
