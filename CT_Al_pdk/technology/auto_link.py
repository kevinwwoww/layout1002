from typing import Tuple

from fnpcell.pdk.technology import all as fpt

from CT_Al_pdk.technology.wg import WG


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
                (type(WG.Strip_WG.C.WIRE) >> type(WG.Strip_WG.C.WIRE), LinkPrefer(WG.Strip_WG.C.WIRE),
                 BendUsing(WG.Strip_WG.C.WIRE.BEND_EULER)),
                (type(WG.Rib_WG.C.WIRE) >> type(WG.Rib_WG.C.WIRE), LinkPrefer(WG.Rib_WG.C.WIRE),
                 BendUsing(WG.Rib_WG.C.WIRE.BEND_EULER)),
                (type(WG.SiN_WG.C.WIRE) >> type(WG.SiN_WG.C.WIRE), LinkPrefer(WG.SiN_WG.C.WIRE),
                 BendUsing(WG.SiN_WG.C.WIRE.BEND_EULER)),

                (type(WG.Strip_WG.O.WIRE) >> type(WG.Strip_WG.O.WIRE), LinkPrefer(WG.Strip_WG.O.WIRE),
                 BendUsing(WG.Strip_WG.O.WIRE.BEND_EULER)),
                (type(WG.Rib_WG.O.WIRE) >> type(WG.Rib_WG.O.WIRE), LinkPrefer(WG.Rib_WG.O.WIRE),
                 BendUsing(WG.Rib_WG.O.WIRE.BEND_EULER)),
                (type(WG.SiN_WG.O.WIRE) >> type(WG.SiN_WG.O.WIRE), LinkPrefer(WG.SiN_WG.O.WIRE),
                 BendUsing(WG.SiN_WG.O.WIRE.BEND_EULER)),

            ]
        )

    DEFAULT = LESS_TRANS
