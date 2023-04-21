import AMFpdk_3_5_Oband
from fnpcell import console
from fnpcell.pdk.technology.all import register_technology

from AMFpdk_3_5_Oband.technology.tech import TECH as AMF_TECH
from AMFpdk_3_5_Oband.technology.wg import WG # type: ignore

console.info(f"AMFpdk_3_5_Oband version: {AMFpdk_3_5_Oband.__version__}")

get_technology = register_technology(AMF_TECH)
