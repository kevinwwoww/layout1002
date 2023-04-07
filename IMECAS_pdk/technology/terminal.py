from fnpcell import all as fp


class PIN:
    LENGTH = 0.5
    OFFSET = -0.25

    @staticmethod
    def ICON_LAYER(layer: fp.IMetalLineType):
        from . import get_technology

        return get_technology().LAYER.PINREC

    @staticmethod
    def TEXT_LAYER(layer: fp.IMetalLineType):
        from . import get_technology

        return get_technology().LAYER.PINREC


class PORT:
    LENGTH = 0.5
    OFFSET = -0.25

    @staticmethod
    def ICON_LAYER(waveguide_type: fp.IWaveguideType):
        from . import get_technology

        LAYER = get_technology().LAYER
        layer: ILayer = waveguide_type.core_layer  # type: ignore
        if layer == LAYER.FECOR:
            return LAYER.PINREC
        elif layer == LAYER.SECOR:
            return LAYER.PINREC
        elif layer == LAYER.MECOR:
            return LAYER.PINREC
        else:
            return LAYER.PINREC



    @staticmethod
    def TEXT_LAYER(waveguide_type: fp.IWaveguideType):
        from . import get_technology

        return get_technology().LAYER.DOC
