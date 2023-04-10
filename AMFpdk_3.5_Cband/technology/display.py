from AMFpdk_3_5_Cband.technology.layers import LAYER
from fnpcell.pdk.technology.all import FillPattern, LayerFill, LayerStroke, LayerStyle, LayerStyleSet, NamedColor

class DISPLAY:

    LAYER_STYLE = LayerStyleSet.random(LAYER).updated(
        {
            LAYER.RIB: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.GRAT: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.CYAN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.CYAN,
                    width=1,
                ),
            ),
            LAYER.SLAB: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.MAGENTA,
                ),
                stroke=LayerStroke(
                    color=NamedColor.MAGENTA,
                    width=1,
                ),
            ),
            LAYER.PP: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.RED,
                ),
                stroke=LayerStroke(
                    color=NamedColor.RED,
                    width=1,
                ),
            ),
            LAYER.PCONT: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.RED1,
                ),
                stroke=LayerStroke(
                    color=NamedColor.RED1,
                    width=1,
                ),
            ),
            LAYER.NCONT: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.DARKOLIVEGREEN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.DARKOLIVEGREEN,
                    width=1,
                ),
            ),
            LAYER.PIM: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.RED2,
                ),
                stroke=LayerStroke(
                    color=NamedColor.RED2,
                    width=1,
                ),
            ),
            LAYER.NIM: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.DARKOLIVEGREEN1,
                ),
                stroke=LayerStroke(
                    color=NamedColor.DARKOLIVEGREEN1,
                    width=1,
                ),
            ),
            LAYER.IPD: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.RED3,
                ),
                stroke=LayerStroke(
                    color=NamedColor.RED3,
                    width=1,
                ),
            ),
            LAYER.IND: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.DARKOLIVEGREEN2,
                ),
                stroke=LayerStroke(
                    color=NamedColor.DARKOLIVEGREEN2,
                    width=1,
                ),
            ),
            LAYER.GeEP: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.ROSYBROWN,
                ),
                stroke=LayerStroke(
                    color=NamedColor.ROSYBROWN,
                    width=1,
                ),
            ),
            LAYER.NPPGE: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.ALICEBLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.ALICEBLUE,
                    width=1,
                ),
            ),
            LAYER.VIA1: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.LIGHTPINK,
                ),
                stroke=LayerStroke(
                    color=NamedColor.LIGHTPINK,
                    width=1,
                ),
            ),
            LAYER.MT1: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.LIGHTBLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.LIGHTBLUE,
                    width=1,
                ),
            ),
            LAYER.HTR: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.LIGHTGRAY,
                ),
                stroke=LayerStroke(
                    color=NamedColor.LIGHTGRAY,
                    width=1,
                ),
            ),
            LAYER.VIA2: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.LIGHTCORAL,
                ),
                stroke=LayerStroke(
                    color=NamedColor.LIGHTCORAL,
                    width=1,
                ),
            ),
            LAYER.MT2: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.LIGHTSALMON,
                ),
                stroke=LayerStroke(
                    color=NamedColor.LIGHTSALMON,
                    width=1,
                ),
            ),
            LAYER.PAD: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.OX_OPEN: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.DT: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.TR: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.TM1: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.EXCL: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.LBL: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.MARKER: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
            LAYER.BLACK_FP: LayerStyle(
                fill=LayerFill(
                    pattern=FillPattern.DIAGONAL,
                    color=NamedColor.BLUE,
                ),
                stroke=LayerStroke(
                    color=NamedColor.BLUE,
                    width=1,
                ),
            ),
        }
    )