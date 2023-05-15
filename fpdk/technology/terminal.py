from fnpcell import all as fp


class PIN:
    LENGTH = 0.3
    OFFSET = -0.15

    @staticmethod
    def ICON_LAYER(layer: fp.IMetalLineType):
        from . import get_technology

        return get_technology().LAYER.PINREC_NOTE

    @staticmethod
    def TEXT_LAYER(layer: fp.IMetalLineType):
        from . import get_technology

        return get_technology().LAYER.PINREC_TEXT


class PORT:
    LENGTH = 0.3
    OFFSET = -0.15

    @staticmethod
    def ICON_LAYER(waveguide_type: fp.IWaveguideType):
        from . import get_technology

        LAYER = get_technology().LAYER
        layer: ILayer = waveguide_type.core_layer  # type: ignore
        if layer == LAYER.FWG_COR:
            return LAYER.PINREC_FWG
        elif layer == LAYER.SWG_COR:
            return LAYER.PINREC_SWG
        elif layer == LAYER.MWG_COR:
            return LAYER.PINREC_MWG
        else:
            return LAYER.PINREC_NOTE

    @staticmethod
    def TEXT_LAYER(waveguide_type: fp.IWaveguideType):
        from . import get_technology

        return get_technology().LAYER.PINREC_TEXT
