import AMFpdk_3_5_Cband_0420
from fnpcell import console
from fnpcell.pdk.technology.all import register_technology

from AMFpdk_3_5_Cband_0420.technology.tech import TECH as AMF_TECH
from AMFpdk_3_5_Cband_0420.technology.wg import WG # type: ignore

console.info(f"AMFpdk_3_5_Cband_0420 version: {AMFpdk_3_5_Cband_0420.__version__}")

get_technology = register_technology(AMF_TECH)
