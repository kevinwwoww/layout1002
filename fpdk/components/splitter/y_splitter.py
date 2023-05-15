from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from fpdk.components.straight.straight import Straight
from fpdk.components.bend.bend_euler import BendEuler
from fpdk.components.taper.taper_linear import TaperLinear
from fpdk.technology import get_technology
from fpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class YSplitter(fp.PCell):
    """
    Attributes:
        bend_radius: defaults to 15, Bend radius
        out_degrees: defaults to 90, Angle at which the waveguide exit the splitter
        center_waveguide_length: defaults to 2.0, Length of the center waveguide
        taper_length: defaults to 0.1, Length of the tapered section
        waveguide_type: type of waveguide
        port_names: defaults to ["op_0", "op_1", "op_2"]

    Examples:
    ```python
    TECH = get_technology()
    splitter = YSplitter(waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(splitter)
    ```
    ![YSplitter](images/y_splitter.png)
    """

    bend_radius: float = fp.PositiveFloatParam(default=15, doc="Bend radius")
    out_degrees: float = fp.DegreeParam(default=90, doc="Angle at which the waveguide exit the splitter")
    center_waveguide_length: float = fp.PositiveFloatParam(default=2.0, doc="Length of the center waveguide")
    taper_length: float = fp.PositiveFloatParam(default=0.1, doc="Length of the tapered section")
    waveguide_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=3, default=("op_0", "op_1", "op_2"))

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()

        # fmt: off

        bend_radius = self.bend_radius
        out_degrees = self.out_degrees
        center_waveguide_length = self.center_waveguide_length
        taper_length = self.taper_length
        waveguide_type = self.waveguide_type
        port_names = self.port_names

        core_width = waveguide_type.core_width

        # center_type = waveguide_type.updated(cladding_layout_width=waveguide_type.cladding_width + core_width)
        # cancel center_type for auto_link
        center = Straight(length=center_waveguide_length, waveguide_type=waveguide_type, anchor=fp.Anchor.END, transform=fp.translate(-taper_length, 0))
        insts += center
        ports += center["op_0"].with_name(port_names[0])

        taper_type = waveguide_type.updated(core_layout_width=core_width * 2, cladding_layout_width=waveguide_type.cladding_width + core_width)
        taper = TaperLinear(length=taper_length, left_type=waveguide_type, right_type=taper_type, anchor=fp.Anchor.END)
        insts += taper

        # bend_top = fp.Waveguide(type=waveguide_type, curve=fp.g.CircularBend(radius=bend_radius, degrees=out_degrees, origin=(0, core_width / 2)))
        bend_top = BendEuler(radius_eff=bend_radius, degrees=out_degrees, waveguide_type=waveguide_type).translated(0, core_width/2)
        insts += bend_top
        # ports += bend_top["op_1"].with_name(port_names[2])
        bend_bottom = bend_top.v_mirrored()
        insts += bend_bottom
        ports += bend_bottom["op_1"].with_name(port_names[1])
        ports += bend_top["op_1"].with_name(port_names[2])  # for right port index(0 1 2) in netlist

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from fpdk.components import all as components
    from fpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += YSplitter()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=components)
    # fp.plot(library)
