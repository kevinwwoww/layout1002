from typing import Tuple

from fnpcell.pdk.technology import all as fpt

from IMECAS_SiN_pdk.technology.wg import WG


class LinkPrefer:
    def __init__(self, link_type: fpt.IWaveguideType):
        self.link_type = link_type

    def __call__(self, end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]) -> fpt.IWaveguideType:
        link_type = self.link_type
        a, b = end_types
        if a == b and a != link_type:
            return a
        return link_type


class BendUsing:
    def __init__(self, bend_factory: fpt.IBendWaveguideFactory):
        self.bend_factory = bend_factory

    def __call__(self, _end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]) -> fpt.IBendWaveguideFactory:
        return self.bend_factory


class LINKING_POLICY:
    @fpt.classconst
    @classmethod
    def LESS_TRANS(cls):
        return fpt.LinkingPolicy().updated(
            [
                #
                (type(WG.Channel.C.WIRE) >> type(WG.Channel.C.WIRE), LinkPrefer(WG.Channel.C.WIRE), BendUsing(WG.Channel.C.WIRE.BEND)),
                (type(WG.Channel.O.WIRE) >> type(WG.Channel.O.WIRE), LinkPrefer(WG.Channel.O.WIRE), BendUsing(WG.Channel.O.WIRE.BEND)),
                #
            ]
        )

    DEFAULT = LESS_TRANS
