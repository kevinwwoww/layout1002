from fnpcell.pdk.technology import all as fpt
from gpdk.technology.tech import TECH as GPDK_TECH

from .layers import LAYER


class DISPLAY(GPDK_TECH.DISPLAY):
    LAYER_STYLE = GPDK_TECH.DISPLAY.LAYER_STYLE.updated(
        {
            LAYER.TIN_DRW: fpt.LayerStyle(
                fill=fpt.LayerFill(
                    pattern=fpt.FillPattern.DIAGONAL,
                    color=fpt.Color(1, 0, 0, 0.5),
                ),
                stroke=fpt.LayerStroke(
                    color=fpt.Color(0.1, 0.3, 0.2, 0.5),
                    width=1,
                ),
            ),
        }
    )
