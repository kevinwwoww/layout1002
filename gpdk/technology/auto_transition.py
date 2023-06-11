from typing import Tuple, cast
from dataclasses import dataclass
from fnpcell.pdk.technology import all as fpt
from fnpcell import all as fp
from .interfaces import CoreCladdingWaveguideType
from .wg import WG

SLOPE = 0.2


@dataclass(eq=False)
class FWG2MWG(fp.ICurvedCellRef, fp.PCell):
    end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType] = fp.Param()

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()

        a = self.end_types[0]
        b = self.end_types[1]
        assert isinstance(a, WG.FWG.C)
        assert isinstance(b, WG.MWG.C)
        if a == WG.FWG.C.WIRE and b == WG.MWG.C.WIRE:
            from ..components.transition.fwg2mwg_transition import FWG_WIRE2MWG_WIRETransition

            cell = FWG_WIRE2MWG_WIRETransition()

        elif a == WG.FWG.C.EXPANDED and b == WG.MWG.C.EXPANDED:
            from ..components.transition.fwg2mwg_transition import FWG_EXPANDED2MWG_EXPANDEDTransition

            cell = FWG_EXPANDED2MWG_EXPANDEDTransition()

        elif a == WG.FWG.C.WIRE and b == WG.MWG.C.EXPANDED:
            from ..components.transition.fwg2mwg_transition import FWG_WIRE2MWG_WIRETransition
            from ..components.taper.taper_linear import TaperLinear

            transition = FWG_WIRE2MWG_WIRETransition()
            k = SLOPE
            length = max(0.01, abs(WG.MWG.C.EXPANDED.core_width - WG.MWG.C.WIRE.core_width) / k)
            taper = TaperLinear(length=length, left_type=WG.MWG.C.EXPANDED, right_type=WG.MWG.C.WIRE)
            cell = fp.Connected(
                joints=[taper["op_1"] <= transition["op_1"]],
                ports=[taper["op_0"].with_name("op_1"), transition["op_0"].with_name("op_0")],
            )
        elif a == WG.FWG.C.EXPANDED and b == WG.MWG.C.WIRE:
            from ..components.transition.fwg2mwg_transition import FWG_WIRE2MWG_WIRETransition
            from ..components.taper.taper_linear import TaperLinear

            transition = FWG_WIRE2MWG_WIRETransition()
            k = SLOPE
            length = max(0.01, abs(WG.FWG.C.EXPANDED.core_width - WG.FWG.C.WIRE.core_width) / k)
            taper = TaperLinear(length=length, left_type=WG.FWG.C.WIRE, right_type=WG.FWG.C.EXPANDED)
            cell = fp.Connected(
                joints=[taper["op_0"] <= transition["op_0"]],
                ports=[taper["op_1"].with_name("op_0"), transition["op_1"].with_name("op_1")],
            )
        else:  # for old code compatibility
            from ..components.transition.fwg2mwg_transition import FWG2MWGTransition

            cell = FWG2MWGTransition(name="auto", length=20, fwg_type=a, mwg_type=b)
        insts += cell
        ports += cell.ports
        return insts, elems, ports

    @property
    def raw_curve(self):
        IN, OUT = self.cell.ports
        return fp.g.LineBetween(IN.position, OUT.position)


def _c_fwg2mwg(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.FWG.C)
    assert isinstance(b, WG.MWG.C)
    transition = FWG2MWG(end_types=end_types)

    return transition, ("op_0", "op_1")


def _c_fwg2swg(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    from ..components.transition.fwg2swg_transition import FWG2SWGTransition

    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.FWG.C)
    assert isinstance(b, WG.SWG.C)

    return FWG2SWGTransition(name="auto", length=20, fwg_type=a, swg_type=b), ("op_0", "op_1")


def _c_swg2mwg(end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
    from ..components.transition.swg2mwg_transition import SWG2MWGTransition

    a = end_types[0]
    b = end_types[1]
    assert isinstance(a, WG.SWG.C)
    assert isinstance(b, WG.MWG.C)

    return SWG2MWGTransition(name="auto", swg_length=10, mwg_length=10, swg_type=a, mwg_type=b), ("op_0", "op_1")


class _Taper:
    def __init__(self, slope: float) -> None:
        self.slope = slope

    def __call__(self, end_types: Tuple[fpt.IWaveguideType, fpt.IWaveguideType]):
        from ..components.taper.taper_linear import TaperLinear

        a = cast(CoreCladdingWaveguideType, end_types[0])
        b = cast(CoreCladdingWaveguideType, end_types[1])
        k = self.slope
        length = max(0.01, abs(a.core_width - b.core_width) / k)
        return TaperLinear(name="auto", length=length, left_type=a, right_type=b), ("op_0", "op_1")


class AUTO_TRANSITION:
    @fpt.classconst
    @classmethod
    def DEFAULT(cls):
        return fpt.AutoTransition().updated(
            [
                (WG.FWG.C >> WG.MWG.C, _c_fwg2mwg),
                (WG.FWG.C >> WG.SWG.C, _c_fwg2swg),
                (WG.SWG.C >> WG.MWG.C, _c_swg2mwg),
                #
                (WG.FWG.C >> WG.FWG.C, _Taper(SLOPE)),
                (WG.SWG.C >> WG.SWG.C, _Taper(SLOPE)),
                (WG.MWG.C >> WG.MWG.C, _Taper(SLOPE)),
            ]
        )
