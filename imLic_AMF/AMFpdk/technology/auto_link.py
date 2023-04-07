from typing import Tuple

from fnpcell.pdk.technology import all as fpt

from AMFpdk.technology.wg import WG


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
                (type(WG.RIB.C.WIRE) >> type(WG.RIB.C.WIRE), LinkPrefer(WG.RIB.C.WIRE),
                 BendUsing(WG.RIB.C.WIRE.BEND_CIRCULAR)),
                (type(WG.GRAT.C.WIRE) >> type(WG.GRAT.C.WIRE), LinkPrefer(WG.GRAT.C.WIRE),
                 BendUsing(WG.GRAT.C.WIRE.BEND_CIRCULAR)),
                (type(WG.SLAB.C.WIRE) >> type(WG.SLAB.C.WIRE), LinkPrefer(WG.SLAB.C.WIRE),
                 BendUsing(WG.SLAB.C.WIRE.BEND_CIRCULAR)),

                (type(WG.RIB.C.WIRE) >> type(WG.GRAT.C.WIRE), LinkPrefer(WG.GRAT.C.WIRE),
                 BendUsing(WG.GRAT.C.WIRE.BEND_CIRCULAR)),
                (type(WG.GRAT.C.WIRE) >> type(WG.SLAB.C.WIRE), LinkPrefer(WG.SLAB.C.WIRE),
                 BendUsing(WG.SLAB.C.WIRE.BEND_CIRCULAR)),
                (type(WG.RIB.C.WIRE) >> type(WG.SLAB.C.WIRE), LinkPrefer(WG.SLAB.C.WIRE),
                 BendUsing(WG.SLAB.C.WIRE.BEND_CIRCULAR)),
            ]
        )

    DEFAULT = LESS_TRANS
