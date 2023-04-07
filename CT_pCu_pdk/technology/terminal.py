from fnpcell import all as fp
from fnpcell.interfaces import ILayer


class PORT:
    LENGTH = 0.3
    OFFSET = -0.15

    @staticmethod
    def ICON_LAYER(waveguide_type: fp.IWaveguideType):
        from CT_pCu_pdk.technology import get_technology

        LAYER = get_technology().LAYER
        layer: ILayer = waveguide_type.wg_layer
        if layer == LAYER.Hard_Mask_WG:
            return LAYER.PINREC_HM_WG
        elif layer == LAYER.Rib_WG:
            return LAYER.PINREC_Rib
        elif layer == LAYER.Strip_WG:
            return LAYER.PINREC_Strip
        elif layer == LAYER.SiN_WG:
            return LAYER.PINREC_SiN
        else:
            return LAYER.PINREC_NOTE



    @staticmethod
    def TEXT_LAYER(waveguide_type: fp.IWaveguideType):
        from CT_pCu_pdk.technology import get_technology

        return get_technology().LAYER.PINREC_TEXT


class PIN:
    LENGTH = 0.3
    OFFSET = -0.15

    @staticmethod
    def ICON_LAYER(layer: fp.IMetalLineType):
        from CT_pCu_pdk.technology import get_technology
        return get_technology().LAYER.PINREC_NOTE

    @staticmethod
    def TEXT_LAYER(layer: fp.IMetalLineType):
        from CT_pCu_pdk.technology import get_technology
        return get_technology().LAYER.PINREC_TEXT
