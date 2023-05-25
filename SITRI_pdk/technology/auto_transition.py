from typing import Tuple, cast
from fnpcell.pdk.technology import all as fpt
from SITRI_pdk.technology.interfaces import CoreWaveguideType
from SITRI_pdk.technology.wg import WG


def _c_channel2slab(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    from SITRI_pdk.components.transition.channel2slab_transition import CHANNEL2SLABTransition

    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.CHANNEL.C)
    assert isinstance(b, WG.SLAB.C)

    return CHANNEL2SLABTransition(name="auto", Length=20, channel_type=a, slab_type=b), ("op_0", "op_1")


class _Taper:
    def __init__(self, slope: float) -> None:
        self.slope = slope

    def __call__(self, end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
        from SITRI_pdk.components.taper.taperH import taperH

        a = cast(CoreWaveguideType, end_types[0])
        b = cast(CoreWaveguideType, end_types[1])
        k = self.slope
        length = max(0.01, abs(a.wg_width - b.wg_width) / k)
        return taperH(name="auto", Length=length, left_type=a, right_type=b), ("op_0", "op_1")


class AUTO_TRANSITION:
    @fpt.classconst
    @classmethod
    def DEFAULT(cls):
        return fpt.AutoTransition().updated(
            [
                (WG.CHANNEL.C >> WG.SLAB.C, _c_channel2slab),

                (WG.CHANNEL.C >> WG.CHANNEL.C, _Taper(0.2)),
                (WG.SLAB.C >> WG.SLAB.C, _Taper(0.2)),
                (WG.SIN.C >> WG.SIN.C, _Taper(0.2)),
            ]
        )
