from typing import Tuple, cast
from fnpcell.pdk.technology import all as fpt
from CT_Al_pdk.technology.interfaces import CoreWaveguideType
from CT_Al_pdk.technology.wg import WG


# Hard_Mask > Strip > Rib

# class AUTO_TRANSITION:
#     @fpt.classconst
#     @classmethod
#     def DEFAULT(cls):
#         return fpt.AutoTransition().updated(
#             [
#                 (WG.Strip_WG.C >> WG.SiN_WG.C, ),
#
#             ]
#         )
