from typing import Tuple, cast
from fnpcell.pdk.technology import all as fpt
from AMFpdk_3_5_Cband.technology.interfaces import CoreWaveguideType
from AMFpdk_3_5_Cband.technology.wg import WG


def _c_grat2slab(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    from AMFpdk_3_5_Cband.components.transition.grat2slab_transition import GRAT2SLABTransition

    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.GRAT.C)
    assert isinstance(b, WG.SLAB.C)

    return GRAT2SLABTransition(name="auto", grat_length=10, slab_length=10, grat_type=a, slab_type=b), ("op_0", "op_1")


def _c_rib2grat(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    from AMFpdk_3_5_Cband.components.transition.rib2grat_transition import RIB2GRATTransition

    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.RIB.C)
    assert isinstance(b, WG.GRAT.C)

    return RIB2GRATTransition(name="auto", length=20, rib_type=a, grat_type=b), ("op_0", "op_1")


def _c_rib2slab(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    from AMFpdk_3_5_Cband.components.transition.rib2slab_transition import RIB2SLABTransition

    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.RIB.C)
    assert isinstance(b, WG.SLAB.C)

    return RIB2SLABTransition(name="auto", length=20, rib_type=a, slab_type=b), ("op_0", "op_1")


class _Taper:
    def __init__(self, slope: float) -> None:
        self.slope = slope

    def __call__(self, end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
        from AMFpdk_3_5_Cband.components.taper.taper_linear import TaperLinear

        a = cast(CoreWaveguideType, end_types[0])
        b = cast(CoreWaveguideType, end_types[1])
        k = self.slope
        length = max(0.01, abs(a.wg_width - b.wg_width) / k)
        return TaperLinear(name="auto", length=length, left_type=a, right_type=b), ("op_0", "op_1")


class AUTO_TRANSITION:
    @fpt.classconst
    @classmethod
    def DEFAULT(cls):
        return fpt.AutoTransition().updated(
            [
                # (WG.RIB.C >> WG.GRAT.C, _c_rib2grat),
                # (WG.RIB.C >> WG.SLAB.C, _c_rib2slab),
                # (WG.GRAT.C >> WG.SLAB.C, _c_grat2slab),

                # (WG.SLAB.C >> WG.SLAB.C, _Taper(0.2)),
                # (WG.RIB.C >> WG.RIB.C, _Taper(0.2)),
                # (WG.GRAT.C >> WG.GRAT.C, _Taper(0.2)),
            ]
        )
