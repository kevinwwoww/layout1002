# Generated from C:\photoCAD\layout1002\fpdk\technology\layers.csv

from fnpcell.pdk.technology.all import FillPattern, LayerFill, LayerStroke, LayerStyle, LayerStyleSet, NamedColor
from .layers import LAYER

class DISPLAY():
    LAYER_STYLE = LayerStyleSet.random(LAYER).updated({LAYER.FWG_COR: LayerStyle(fill=LayerFill(color=NamedColor.BLUE, pattern=FillPattern.DIAGONAL), stroke=LayerStroke(color=NamedColor.BLUE, width=1)), LAYER.FWG_CLD: LayerStyle(fill=LayerFill(color=NamedColor.BLUE, pattern=FillPattern.BACK_DIAGONAL), stroke=LayerStroke(color=NamedColor.BLUE, width=1))})
