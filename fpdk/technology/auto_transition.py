from typing import Tuple, cast
from dataclasses import dataclass
from fnpcell.pdk.technology import all as fpt
from fnpcell import all as fp
from .interfaces import CoreCladdingWaveguideType
from .wg import WG

SLOPE = 0.2


def _c_fwg2swg(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    from ..components.transition.fwg2swg_transition import FWG2SWGTransition

    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.FWG.C)
    assert isinstance(b, WG.SWG.C)

    return FWG2SWGTransition(name="auto", length=20, fwg_type=a, swg_type=b), ("op_0", "op_1")


class _Taper:
    def __init__(self, slope: float) -> None:
        self.slope = slope

    def __call__(self, end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
        from ..components.taper.taper_linear import TaperLinear

        a = cast(CoreCladdingWaveguideType, end_types[0])
        b = cast(CoreCladdingWaveguideType, end_types[1])
        k = self.slope
        length = max(0.01, abs(a.core_width - b.core_width) / k)
        return TaperLinear(name="auto", length=length, left_type=a, right_type=b), ("op_0", "op_1")


class AUTO_TRANSITION:
    @fpt.classconst
    @classmethod
    def DEFAULT(cls):
        return fpt.AutoTransition().updated(
            [
                (WG.FWG.C >> WG.SWG.C, _c_fwg2swg),
                #
                (WG.FWG.C >> WG.FWG.C, _Taper(SLOPE)),
                (WG.SWG.C >> WG.SWG.C, _Taper(SLOPE)),
            ]
        )
