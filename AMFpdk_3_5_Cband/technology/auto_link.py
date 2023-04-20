from typing import Tuple

from fnpcell.pdk.technology import all as fpt

from AMFpdk_3_5_Cband.technology.wg import WG


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
                (type(WG.CHANNEL.C.WIRE) >> type(WG.CHANNEL.C.WIRE), LinkPrefer(WG.CHANNEL.C.WIRE),
                 BendUsing(WG.CHANNEL.C.WIRE.BEND_CIRCULAR)),
                (type(WG.SLAB.C.WIRE) >> type(WG.SLAB.C.WIRE), LinkPrefer(WG.SLAB.C.WIRE),
                 BendUsing(WG.SLAB.C.WIRE.BEND_CIRCULAR)),
                (type(WG.SIN.C.WIRE) >> type(WG.SIN.C.WIRE), LinkPrefer(WG.SIN.C.WIRE),
                 BendUsing(WG.SIN.C.WIRE.BEND_CIRCULAR)),

            ]
        )

    DEFAULT = LESS_TRANS
