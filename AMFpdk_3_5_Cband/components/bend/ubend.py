from dataclasses import dataclass
from functools import cached_property
from typing import Tuple
import math

from fnpcell import all as fp
from fnpcell.interfaces import angle_between, distance_between
from AMFpdk_3_5_Cband.technology import get_technology, WG
from AMFpdk_3_5_Cband.components.bend.bend_circular import Bend90
from AMFpdk_3_5_Cband.components.straight.straight import Straight


@dataclass(eq=False)
class Ubend(fp.IWaveguideLike, fp.PCell):
    Width: float = fp.PositiveFloatParam(default=0.5)
    Radius: float = fp.PositiveFloatParam(default=10)
    sLength: float = fp.NonNegFloatParam(default=0)
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=("op_0", "op_1"))
    bend: fp.IDevice = fp.DeviceParam(type=Bend90, port_count=2, required=True)

    # straight: fp.IDevice = fp.DeviceParam(type=Straight, port_count=2, required=False)

    def _default_waveguide_type(self):
        return get_technology().WG.CHANNEL.C.WIRE.updated(wg_design_width=self.Width)

    def _default_bend(self):
        return Bend90(
            name="bend",
            Radius=self.Radius,
            Width=self.Width,
            waveguide_type=self.waveguide_type
        )

    def build(self):
        insts, elems, ports = super().build()

        Width = self.Width
        Radius = self.Radius
        sLength = self.sLength
        bend = self.bend
        waveguide_type = self.waveguide_type
        port_names = self.port_names
        # straight = self.straight

        bend_right = bend
        bend_left = bend.translated(self.sLength, 0).h_mirrored()
        straight = fp.el.Line(
            length=sLength,
            stroke_width=Width,
            layer=waveguide_type.wg_layer,
            transform=fp.translate(-self.sLength, self.Radius)
        )
        elems += straight
        insts += bend_left, bend_right
        ports += bend_left["op_0"].with_name(port_names[0])
        ports += bend_right["op_0"].with_name(port_names[1])

        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk_3_5_Cband.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    library += Ubend(Width=3, sLength=3)

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
