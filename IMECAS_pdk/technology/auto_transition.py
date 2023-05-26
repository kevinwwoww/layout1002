from typing import Tuple, cast
from fnpcell.pdk.technology import all as fpt

from IMECAS_pdk.technology.wg import WG


def _c_channel2rib(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    from IMECAS_pdk.components.bb_Transition.TR450_rib650 import TR450_rib650

    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.Channel.C)
    assert isinstance(b, WG.Rib.C)

    return TR450_rib650(), ("op_0", "op_1")


def _o_channel2rib(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    from IMECAS_pdk.components.bb_Transition.TR380_Rib580 import TR380_Rib580
    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.Channel.O)
    assert isinstance(b, WG.Rib.O)

    return TR380_Rib580(), ("op_0", "op_1")


class AUTO_TRANSITION:
    @fpt.classconst
    @classmethod
    def DEFAULT(cls):
        return fpt.AutoTransition().updated(
            [
                (WG.Channel.C >> WG.Rib.C, _c_channel2rib),
                (WG.Channel.O >> WG.Rib.O, _o_channel2rib),

                #
            ]
        )
#
