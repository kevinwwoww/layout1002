from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from fnpcell import all as fp
from SITRI_pdk.technology import get_technology
from SITRI_pdk.technology.interfaces import CoreWaveguideType


@dataclass(eq=False)
class taperH(fp.IWaveguideLike, fp.PCell):
    Length: float = fp.PositiveFloatParam(default=5.0)
    leftWidth: float = fp.PositiveFloatParam(default=1.0)
    rightWidth: float = fp.PositiveFloatParam(default=3.0)
    left_type: CoreWaveguideType = fp.WaveguideTypeParam(type=CoreWaveguideType)
    right_type: CoreWaveguideType = fp.WaveguideTypeParam(type=CoreWaveguideType)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.CENTER)
    port_names = fp.IPortOption = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_left_type(self):
        return get_technology().WG.CHANNEL.C.WIRE.updated(wg_design_width=self.leftWidth)

    def _default_right_type(self):
        return get_technology().WG.CHANNEL.C.WIRE.updated(wg_design_width=self.rightWidth)

    @cached_property
    def raw_curve(self):
        return fp.g.Line(
            length=self.Length,
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

    @fp.cache()
    def sim_model(self, env: fp.ISimEnv):
        left_model = self.left_type.theoretical_parameters
        right_model = self.left_type.theoretical_parameters
        return fp.sim.TaperLinearModel([left_model, right_model], length=self.length)


if __name__ == "__main__":
    from SITRI_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    library += taperH()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
