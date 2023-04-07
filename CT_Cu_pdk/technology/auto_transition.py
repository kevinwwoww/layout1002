from typing import Tuple, cast
from fnpcell.pdk.technology import all as fpt
from CT_Cu_pdk.technology.interfaces import CoreWaveguideType
from CT_Cu_pdk.technology.wg import WG


# Hard_Mask > Strip > Rib

def _o_strip2sin(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    from CT_Cu_pdk.components.fixed_tran_si_sin_gap200.fixed_tran_si_sin_gap200_o import tran_si_sin_gap200_o

    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.Strip_WG.O)
    assert isinstance(b, WG.Rib_WG.O)

    return tran_si_sin_gap200_o(), ("op_0", "op_1")


class AUTO_TRANSITION:
    @fpt.classconst
    @classmethod
    def DEFAULT(cls):
        return fpt.AutoTransition().updated(
            [
                (WG.Strip_WG.O >> WG.SiN_WG.O, _o_strip2sin),

            ]
        )
