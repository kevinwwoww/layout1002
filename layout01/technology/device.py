from fnpcell.pdk.technology import all as fpt
from gpdk.technology.tech import TECH as GPDK_TECH


class DEVICE(GPDK_TECH.DEVICE):
    @fpt.classconst
    def BAND_LAYER(cls):
        from . import get_technology

        return get_technology().LAYER.TEXT_NOTE
