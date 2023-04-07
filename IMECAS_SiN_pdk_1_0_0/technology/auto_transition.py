from typing import Tuple, cast

from fnpcell.pdk.technology import all as fpt
from .wg import WG
from .interfaces import CoreCladdingTrenchWaveguideType


class _Taper:
    def __init__(self, slope: float) -> None:
        self.slope = slope

    def __call__(self, end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
        from ..components.taper.taper_linear import TaperLinear

        a = cast(CoreCladdingTrenchWaveguideType, end_types[0])
        b = cast(CoreCladdingTrenchWaveguideType, end_types[1])
        k = self.slope
        length = max(0.01, abs(a.core_width - b.core_width) / k)
        return TaperLinear(name="auto", length=length, left_type=a, right_type=b), ("op_0", "op_1")


class AUTO_TRANSITION:
    @fpt.classconst
    @classmethod
    def DEFAULT(cls):
        return fpt.AutoTransition().updated(
            [
                #
                (WG.Channel.C >> WG.Channel.C, _Taper(0.2)),

            ]
        )