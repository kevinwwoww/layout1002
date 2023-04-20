from typing import Tuple, cast
from fnpcell.pdk.technology import all as fpt
from AMFpdk.technology.interfaces import CoreWaveguideType
from AMFpdk.technology.wg import WG


def _c_channel2rib(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    from AMFpdk.components.transition.channel2rib_transition import CHANNEL2RIBTransition

    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.CHANNEL.C)
    assert isinstance(b, WG.RIB.C)

    return CHANNEL2RIBTransition(name="auto", length=10, channel_type=a, rib_type=b), ("op_0", "op_1")


class _Taper:
    def __init__(self, slope: float) -> None:
        self.slope = slope

    def __call__(self, end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
        from AMFpdk.components.taper.taper_linear import TaperLinear

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

                (WG.CHANNEL.C >> WG.RIB.C, _c_channel2rib),
                #
                # (WG.CHANNEL.C >> WG.CHANNEL.C, _Taper(0.2)),
                # (WG.RIB.C >> WG.RIB.C, _Taper(0.2)),
            ]
        )
