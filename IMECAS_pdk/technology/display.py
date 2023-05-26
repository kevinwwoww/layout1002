# Generated from C:\photoCAD\layout1002\IMECAS_pdk\technology\layers.csv

from fnpcell.pdk.technology.all import FillPattern, LayerFill, LayerStroke, LayerStyle, LayerStyleSet, NamedColor
from IMECAS_pdk.technology.layers import LAYER


class DISPLAY():
    LAYER_STYLE = LayerStyleSet.random(LAYER).updated({LAYER.FECOR: LayerStyle(
        fill=LayerFill(color=NamedColor.BLUE, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.BLUE, width=1)), LAYER.FECLD: LayerStyle(
        fill=LayerFill(color=NamedColor.BLUE, pattern=FillPattern.BACK_DIAGONAL),
        stroke=LayerStroke(color=NamedColor.BLUE, width=1)), LAYER.FETCH: LayerStyle(
        fill=LayerFill(color=NamedColor.BLUE, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.BLUE, width=1)), LAYER.SECOR: LayerStyle(
        fill=LayerFill(color=NamedColor.CYAN, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.CYAN, width=1)), LAYER.SECLD: LayerStyle(
        fill=LayerFill(color=NamedColor.CYAN, pattern=FillPattern.BACK_DIAGONAL),
        stroke=LayerStroke(color=NamedColor.CYAN, width=1)), LAYER.SETCH: LayerStyle(
        fill=LayerFill(color=NamedColor.CYAN, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.CYAN, width=1)), LAYER.MECOR: LayerStyle(
        fill=LayerFill(color=NamedColor.FUCHSIA, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.FUCHSIA, width=1)), LAYER.MECLD: LayerStyle(
        fill=LayerFill(color=NamedColor.FUCHSIA, pattern=FillPattern.BACK_DIAGONAL),
        stroke=LayerStroke(color=NamedColor.FUCHSIA, width=1)), LAYER.METCH: LayerStyle(
        fill=LayerFill(color=NamedColor.FUCHSIA, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.FUCHSIA, width=1)), LAYER.SINSL: LayerStyle(
        fill=LayerFill(color=NamedColor.THISTLE4, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.THISTLE4, width=1)), LAYER.PL: LayerStyle(
        fill=LayerFill(color=NamedColor.DARKVIOLET, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.DARKVIOLET, width=1)), LAYER.NL: LayerStyle(
        fill=LayerFill(color=NamedColor.RED, pattern=FillPattern.BACK_DIAGONAL),
        stroke=LayerStroke(color=NamedColor.RED, width=1)), LAYER.PM: LayerStyle(
        fill=LayerFill(color=NamedColor.GOLDENROD4, pattern=FillPattern.GRID),
        stroke=LayerStroke(color=NamedColor.GOLDENROD4, width=1)), LAYER.NM: LayerStyle(
        fill=LayerFill(color=NamedColor.DARKORANGE3, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.DARKORANGE3, width=1)), LAYER.PH: LayerStyle(
        fill=LayerFill(color=NamedColor.PAPAYAWHIP, pattern=FillPattern.BACK_DIAGONAL),
        stroke=LayerStroke(color=NamedColor.PAPAYAWHIP, width=1)), LAYER.NH: LayerStyle(
        fill=LayerFill(color=NamedColor.SKYBLUE1, pattern=FillPattern.GRID),
        stroke=LayerStroke(color=NamedColor.SKYBLUE1, width=1)), LAYER.GP: LayerStyle(
        fill=LayerFill(color=NamedColor.DARKSEAGREEN, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.DARKSEAGREEN, width=1)), LAYER.GN: LayerStyle(
        fill=LayerFill(color=NamedColor.LAVENDERBLUSH4, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.LAVENDERBLUSH4, width=1)), LAYER.PCON: LayerStyle(
        fill=LayerFill(color=NamedColor.FIREBRICK1, pattern=FillPattern.DOTTED),
        stroke=LayerStroke(color=NamedColor.FIREBRICK1, width=1)), LAYER.GEPCON: LayerStyle(
        fill=LayerFill(color=NamedColor.LIGHTPINK1, pattern=FillPattern.DOTTED),
        stroke=LayerStroke(color=NamedColor.LIGHTPINK1, width=1)), LAYER.GE: LayerStyle(
        fill=LayerFill(color=NamedColor.ROSYBROWN, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.ROSYBROWN, width=1)), LAYER.PY1: LayerStyle(
        fill=LayerFill(color=NamedColor.PEACHPUFF, pattern=FillPattern.BACK_DIAGONAL),
        stroke=LayerStroke(color=NamedColor.PEACHPUFF, width=1)), LAYER.PY2: LayerStyle(
        fill=LayerFill(color=NamedColor.SLATEGRAY, pattern=FillPattern.BACK_DIAGONAL),
        stroke=LayerStroke(color=NamedColor.SLATEGRAY, width=1)), LAYER.M1: LayerStyle(
        fill=LayerFill(color=NamedColor.LIGHTPINK2, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.LIGHTPINK2, width=1)), LAYER.TIN: LayerStyle(
        fill=LayerFill(color=NamedColor.SIENNA3, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.SIENNA3, width=1)), LAYER.PAD: LayerStyle(
        fill=LayerFill(color=NamedColor.LIGHTSALMON4, pattern=FillPattern.GRID),
        stroke=LayerStroke(color=NamedColor.LIGHTSALMON4, width=1)), LAYER.LP: LayerStyle(
        fill=LayerFill(color=NamedColor.CORAL4, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.CORAL4, width=1)), LAYER.DETCH: LayerStyle(
        fill=LayerFill(color=NamedColor.GRAY11, pattern=FillPattern.GRID),
        stroke=LayerStroke(color=NamedColor.GRAY11, width=1)), LAYER.MARK: LayerStyle(
        fill=LayerFill(color=NamedColor.CYAN4, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.CYAN4, width=1)), LAYER.BB: LayerStyle(
        fill=LayerFill(color=NamedColor.LINEN, pattern=FillPattern.BACK_DIAGONAL),
        stroke=LayerStroke(color=NamedColor.LINEN, width=1)), LAYER.DOC: LayerStyle(
        fill=LayerFill(color=NamedColor.LIGHTSEAGREEN, pattern=FillPattern.DIAGONAL),
        stroke=LayerStroke(color=NamedColor.LIGHTSEAGREEN, width=1)), LAYER.PINREC: LayerStyle(
        fill=LayerFill(color=NamedColor.GRAY28, pattern=FillPattern.BACK_DIAGONAL),
        stroke=LayerStroke(color=NamedColor.GRAY28, width=1)), LAYER.FLYLINE_MARK: LayerStyle(
        fill=LayerFill(color=NamedColor.RED, pattern=FillPattern.GRID),
        stroke=LayerStroke(color=NamedColor.RED, width=1)), LAYER.ERROR_MARK: LayerStyle(
        fill=LayerFill(color=NamedColor.YELLOW, pattern=FillPattern.BACK_DIAGONAL),
        stroke=LayerStroke(color=NamedColor.YELLOW, width=1))})
