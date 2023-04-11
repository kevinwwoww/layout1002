from fnpcell import all as fp
from fnpcell.interfaces import ILayer


class PORT:
    LENGTH = 0.5
    OFFSET = -0.25

    @staticmethod
    def ICON_LAYER(waveguide_type: fp.IWaveguideType):
        from AMFpdk_3_5_Cband.technology import get_technology

        LAYER = get_technology().LAYER
        layer: ILayer = waveguide_type.wg_layer
        return LAYER.LBL

    @staticmethod
    def TEXT_LAYER(waveguide_type: fp.IWaveguideType):
        from AMFpdk_3_5_Cband.technology import get_technology

        return get_technology().LAYER.MARKER


class PIN:
    LENGTH = 0.3
    OFFSET = -0.15

    @staticmethod
    def ICON_LAYER(layer: fp.IMetalLineType):
        from AMFpdk_3_5_Cband.technology import get_technology
        return get_technology().LAYER.LBL

    @staticmethod
    def TEXT_LAYER(layer: fp.IMetalLineType):
        from AMFpdk_3_5_Cband.technology import get_technology
        return get_technology().LAYER.MARKER
