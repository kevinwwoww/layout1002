from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from fnpcell import all as fp
from IMECAS_SiN_pdk.technology import get_technology
from IMECAS_SiN_pdk.technology.interfaces import CoreCladdingTrenchWaveguideType

@dataclass(eq=False)
class TaperLinear(fp.IWaveguideLike, fp.PCell):

    length: float = fp.PositiveFloatParam(default=10)
    left_type: CoreCladdingTrenchWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingTrenchWaveguideType)
    right_type: CoreCladdingTrenchWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingTrenchWaveguideType)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.CENTER)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_left_type(self):
        return get_technology().WG.Channel.C.WIRE

    def _default_right_type(self):
        return get_technology().WG.Channel.C.WIRE


    @cached_property
    def raw_curve(self):
        return fp.g.Line(
            length=self.length,
            anchor=self.anchor,
        )

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        assert self.left_type.is_isomorphic_to(self.right_type), "left_type must be isomorphic to right_type"

        wgt = self.left_type.tapered(taper_function=fp.TaperFunction.LINEAR, final_type=self.right_type)
        wg = wgt(curve=self.raw_curve).with_ports(self.port_names)
        insts += wg
        ports += wg.ports
        return insts, elems, ports


if __name__ == "__main__":
    from IMECAS_SiN_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += TaperLinear()

    # fmt: on
    # =============================================================
    # fp.export_gds(library, file=gds_file)
    fp.plot(library)