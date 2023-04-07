# Generated from C:\photoCAD\layout1002\IMECAS_SiN_pdk\technology\layers.csv

from fnpcell.pdk.technology.all import FillPattern, LayerFill, LayerStroke, LayerStyle, LayerStyleSet, NamedColor
from .layers import LAYER

class DISPLAY():
    LAYER_STYLE = LayerStyleSet.random(LAYER).updated({LAYER.SINCOR: LayerStyle(fill=LayerFill(color=NamedColor.BLUE, pattern=FillPattern.DIAGONAL), stroke=LayerStroke(color=NamedColor.BLUE, width=1)), LAYER.SINCLD: LayerStyle(fill=LayerFill(color=NamedColor.BLUE, pattern=FillPattern.BACK_DIAGONAL), stroke=LayerStroke(color=NamedColor.BLUE, width=1)), LAYER.SINTCH: LayerStyle(fill=LayerFill(color=NamedColor.BLUE, pattern=FillPattern.DIAGONAL), stroke=LayerStroke(color=NamedColor.BLUE, width=1)), LAYER.BB: LayerStyle(fill=LayerFill(color=NamedColor.LINEN, pattern=FillPattern.GRID), stroke=LayerStroke(color=NamedColor.LINEN, width=1)), LAYER.DOC: LayerStyle(fill=LayerFill(color=NamedColor.LIGHTSEAGREEN, pattern=FillPattern.DIAGONAL), stroke=LayerStroke(color=NamedColor.LIGHTSEAGREEN, width=1)), LAYER.PINREC: LayerStyle(fill=LayerFill(color=NamedColor.GRAY28, pattern=FillPattern.BACK_DIAGONAL), stroke=LayerStroke(color=NamedColor.GRAY28, width=1)), LAYER.FLYLINE_MARK: LayerStyle(fill=LayerFill(color=NamedColor.RED, pattern=FillPattern.GRID), stroke=LayerStroke(color=NamedColor.RED, width=1)), LAYER.ERROR_MARK: LayerStyle(fill=LayerFill(color=NamedColor.YELLOW, pattern=FillPattern.BACK_DIAGONAL), stroke=LayerStroke(color=NamedColor.YELLOW, width=1))})
