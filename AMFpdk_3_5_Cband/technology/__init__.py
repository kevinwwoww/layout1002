import AMFpdk
from fnpcell import console
from fnpcell.pdk.technology.all import register_technology

from AMFpdk.technology.tech import TECH as AMF_TECH
from AMFpdk.technology.wg import WG # type: ignore

console.info(f"AMFPDK version: {AMFpdk.__version__}")

get_technology = register_technology(AMF_TECH)
