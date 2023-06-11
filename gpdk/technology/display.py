from fnpcell.pdk.technology.all import FillPattern, LayerFill, LayerStroke, LayerStyle, LayerStyleSet, NamedColor

from .layers import LAYER


class DISPLAY:

    LAYER_STYLE = LayerStyleSet.random(LAYER).updated(
        {
            LAYER.FWG_COR: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.FWG_CLD: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.FWG_TRE: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.FWG_HOL: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.SWG_COR: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.CYAN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.CYAN,
                    width=1,
                ),
            ),
            LAYER.SWG_CLD: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.CYAN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.CYAN,
                    width=1,
                ),
            ),
            LAYER.SWG_TRE: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.CYAN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.CYAN,
                    width=1,
                ),
            ),
            LAYER.SWG_HOL: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.GREEN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.GREEN,
                    width=1,
                ),
            ),
            LAYER.MWG_COR: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.MAGENTA,
                ),
                stroke=LayerStroke(
                    color=NamedColor.MAGENTA,
                    width=1,
                ),
            ),
            LAYER.MWG_CLD: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.MAGENTA,
                ),
                stroke=LayerStroke(
                    color=NamedColor.MAGENTA,
                    width=1,
                ),
            ),
            LAYER.MWG_TRE: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.MAGENTA,
                ),
                stroke=LayerStroke(
                    color=NamedColor.MAGENTA,
                    width=1,
                ),
            ),
            LAYER.MWG_HOL: LayerStyle(
                fill=LayerFill(pattern=FillPattern.BACK_DIAGONAL, color=NamedColor.MAGENTA),
                stroke=LayerStroke(
                    color=NamedColor.MAGENTA,
                    width=1,
                ),
            ),
            LAYER.NP_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.DARKVIOLET,
                ),
                stroke=LayerStroke(
                    color=NamedColor.DARKVIOLET,
                    width=1,
                ),
            ),
            LAYER.PP_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.RED,
                ),
                stroke=LayerStroke(
                    color=NamedColor.RED,
                    width=1,
                ),
            ),
            LAYER.NPP_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.DARKVIOLET,
                ),
                stroke=LayerStroke(
                    color=NamedColor.DARKVIOLET,
                    width=1,
                ),
            ),
            LAYER.PPP_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.RED,
                ),
                stroke=LayerStroke(
                    color=NamedColor.RED,
                    width=1,
                ),
            ),
            LAYER.GE_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.ROSYBROWN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.ROSYBROWN,
                    width=1,
                ),
            ),
            LAYER.SIL_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.MAGENTA,
                ),
                stroke=LayerStroke(
                    color=NamedColor.MAGENTA,
                    width=1,
                ),
            ),
            LAYER.TIN_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.SIENNA3,
                ),
                stroke=LayerStroke(
                    color=NamedColor.SIENNA3,
                    width=1,
                ),
            ),
            LAYER.CONT_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.LIGHTPINK2,
                ),
                stroke=LayerStroke(
                    color=NamedColor.LIGHTPINK2,
                    width=1,
                ),
            ),
            LAYER.M1_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.LIGHTPINK2,
                ),
                stroke=LayerStroke(
                    color=NamedColor.LIGHTPINK2,
                    width=1,
                ),
            ),
            LAYER.VIA1_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.CYAN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.CYAN,
                    width=1,
                ),
            ),
            LAYER.MT_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.DARKCYAN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.DARKCYAN,
                    width=1,
                ),
            ),
            LAYER.PASS_EC: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.DARKCYAN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.DARKCYAN,
                    width=1,
                ),
            ),
            LAYER.PASS_GC: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.DARKCYAN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.DARKCYAN,
                    width=1,
                ),
            ),
            LAYER.DEVREC_NOTE: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.DARKCYAN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.DARKCYAN,
                    width=1,
                ),
            ),
            LAYER.PINREC_NOTE: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.DARKCYAN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.DARKCYAN,
                    width=1,
                ),
            ),
            LAYER.IOPORT_OREC: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.LAVENDERBLUSH4,
                ),
                stroke=LayerStroke(
                    color=NamedColor.LAVENDERBLUSH4,
                    width=1,
                ),
            ),
            LAYER.IOPORT_EREC: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.ORANGERED,
                ),
                stroke=LayerStroke(
                    color=NamedColor.ORANGERED,
                    width=1,
                ),
            ),
            LAYER.TEXT_NOTE: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.LIGHTSEAGREEN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.LIGHTSEAGREEN,
                    width=1,
                ),
            ),
            LAYER.TH_ISO_DRW: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.DARKSEAGREEN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.DARKSEAGREEN,
                    width=1,
                ),
            ),
            LAYER.FLYLINE_MARK: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.GRID,
                    color=NamedColor.RED,
                ),
                stroke=LayerStroke(
                    color=NamedColor.RED,
                    width=1,
                ),
            ),
            LAYER.ERROR_MARK: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.BACK_DIAGONAL,
                    color=NamedColor.YELLOW,
                ),
                stroke=LayerStroke(
                    color=NamedColor.YELLOW,
                    width=1,
                ),
            ),
        }
    )
