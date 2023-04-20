from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk.components.straight.straight import Straight
from AMFpdk.components.bend.bend_circular import BendCircular
from AMFpdk.components.taper.taper_linear import TaperLinear
from AMFpdk.technology import get_technology
from AMFpdk.technology.interfaces import CoreWaveguideType


@dataclass(eq=False)
class YSplitter(fp.PCell):
    bend_radius: float = fp.PositiveFloatParam(default=15, doc="Bend Radius")
    out_degrees: float = fp.DegreeParam(default=90, doc="Angle at which the waveguide exit the splitter")
    center_waveguide_length: float = fp.PositiveFloatParam(default=2.0, doc="Length of the center waveguide")
    taper_length: float = fp.PositiveFloatParam(default=0.1, doc="Length of the tapered section")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=3, default=("op_0", "op_1", "op_2"))

    def _default_waveguide_type(self):
        return get_technology().WG.CHANNEL.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()

        bend_radius = self.bend_radius
        out_degrees = self.out_degrees
        center_waveguide_length = self.center_waveguide_length
        taper_length = self.taper_length
        waveguide_type = self.waveguide_type
        port_names = self.port_names

        wg_width = waveguide_type.wg_width

        center = Straight(length=center_waveguide_length, waveguide_type=waveguide_type, anchor=fp.Anchor.END,
                          transform=fp.translate(-taper_length, 0))
        insts += center
        ports += center["op_0"].with_name(port_names[0])

        taper_type = waveguide_type.updated(wg_layout_width=wg_width * 2)
        taper = TaperLinear(length=taper_length, left_type=waveguide_type, right_type=taper_type, anchor=fp.Anchor.END)
        insts += taper

        bend_bottom = BendCircular(radius=bend_radius, degrees=out_degrees, waveguide_type=waveguide_type).translated(0, -15-wg_width / 2)
        # bend_top = BendCircular(radius=bend_radius, degrees=out_degrees, waveguide_type=waveguide_type).translated(0, wg_width / 2)

        insts += bend_bottom

        bend_top = bend_bottom.v_mirrored()
        insts += bend_top

        ports += bend_bottom["op_0"].with_name(port_names[1])
        ports += bend_top["op_0"].with_name(port_names[2])

        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += YSplitter()

    # fp.export_gds(library, file=gds_file)
    fp.plot(library)
