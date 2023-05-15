from typing import Tuple

from fnpcell.pdk.technology import all as fpt

from fpdk.technology.wg import WG


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
                # from >> to,  default link_type, default bend_factory
                #
                # (WG.FWG.C.WIRE >> WG.FWG.C.WIRE, LinkPrefer(WG.FWG.C.WIRE), BendUsing(WG.FWG.C.WIRE.BEND_EULER)),
                #
                # general rules for waveguides (including non-standard waveguides)
                #
                (type(WG.FWG.C.WIRE) >> type(WG.FWG.C.WIRE), LinkPrefer(WG.FWG.C.WIRE), BendUsing(WG.FWG.C.WIRE.BEND_EULER)),
                (type(WG.SWG.C.WIRE) >> type(WG.SWG.C.WIRE), LinkPrefer(WG.SWG.C.WIRE), BendUsing(WG.SWG.C.WIRE.BEND_EULER)),
                #
                (type(WG.FWG.C.WIRE) >> type(WG.SWG.C.WIRE), LinkPrefer(WG.SWG.C.WIRE), BendUsing(WG.SWG.C.WIRE.BEND_EULER)),
                #
                (type(WG.FWG.C.WIRE) >> type(WG.FWG.C.EXPANDED), LinkPrefer(WG.FWG.C.EXPANDED), BendUsing(WG.FWG.C.WIRE.BEND_EULER)),
                (type(WG.SWG.C.WIRE) >> type(WG.SWG.C.EXPANDED), LinkPrefer(WG.SWG.C.EXPANDED), BendUsing(WG.SWG.C.WIRE.BEND_EULER)),
                #
                (type(WG.FWG.C.WIRE) >> type(WG.SWG.C.EXPANDED), LinkPrefer(WG.SWG.C.EXPANDED), BendUsing(WG.SWG.C.EXPANDED.BEND_EULER)),
                #
                (type(WG.FWG.C.EXPANDED) >> type(WG.FWG.C.EXPANDED), LinkPrefer(WG.FWG.C.EXPANDED), BendUsing(WG.FWG.C.WIRE.BEND_EULER)),
                (type(WG.SWG.C.EXPANDED) >> type(WG.SWG.C.EXPANDED), LinkPrefer(WG.SWG.C.EXPANDED), BendUsing(WG.SWG.C.WIRE.BEND_EULER)),
                #
                (type(WG.FWG.C.EXPANDED) >> type(WG.SWG.C.EXPANDED), LinkPrefer(WG.SWG.C.EXPANDED), BendUsing(WG.SWG.C.EXPANDED.BEND_EULER)),
                #
            ]
        )

    @fpt.classconst
    @classmethod
    def MAX_SWG(cls):
        return fpt.LinkingPolicy().updated(
            [
                #
                # from >> to,  default link_type, default bend_factory
                #
                # (WG.FWG.C.WIRE >> WG.FWG.C.WIRE, LinkPrefer(WG.FWG.C.WIRE), BendUsing(WG.FWG.C.WIRE.BEND_EULER)),
                #
                # general rules for waveguides (including non-standard waveguides)
                #
                (type(WG.FWG.C.WIRE) >> type(WG.FWG.C.WIRE), LinkPrefer(WG.SWG.C.EXPANDED), BendUsing(WG.FWG.C.WIRE.BEND_EULER)),
                (type(WG.SWG.C.WIRE) >> type(WG.SWG.C.WIRE), LinkPrefer(WG.SWG.C.EXPANDED), BendUsing(WG.FWG.C.WIRE.BEND_EULER)),
                #
                (type(WG.FWG.C.WIRE) >> type(WG.SWG.C.WIRE), LinkPrefer(WG.SWG.C.EXPANDED), BendUsing(WG.FWG.C.WIRE.BEND_EULER)),
                #
                (type(WG.FWG.C.EXPANDED) >> type(WG.FWG.C.EXPANDED), LinkPrefer(WG.SWG.C.EXPANDED), BendUsing(WG.FWG.C.WIRE.BEND_EULER)),
                (type(WG.SWG.C.EXPANDED) >> type(WG.SWG.C.EXPANDED), LinkPrefer(WG.SWG.C.EXPANDED), BendUsing(WG.FWG.C.WIRE.BEND_EULER)),
                #
                (type(WG.FWG.C.EXPANDED) >> type(WG.SWG.C.EXPANDED), LinkPrefer(WG.SWG.C.EXPANDED), BendUsing(WG.FWG.C.WIRE.BEND_EULER)),
                #
            ]
        )

    DEFAULT = LESS_TRANS
