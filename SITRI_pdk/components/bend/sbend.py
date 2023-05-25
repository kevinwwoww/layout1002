from dataclasses import dataclass
from functools import cached_property
from typing import Tuple
import math

import numpy
from fnpcell import all as fp
from fnpcell.interfaces import angle_between, distance_between
from SITRI_pdk.technology import get_technology, WG
from SITRI_pdk.components.bend.bend_circular import Bend, Bend90
from SITRI_pdk.components.straight.straight import Straight, StraightBetween


@dataclass(eq=False)
class Sbend(fp.IWaveguideLike, fp.PCell):
    Width: float = fp.PositiveFloatParam(default=0.5)
    sHeight: float = fp.NonNegFloatParam(default=10.0)
    sLength: float = fp.NonNegFloatParam(default=10.0)
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=("op_0", "op_1"))
    # bend: fp.IDevice = fp.DeviceParam(type=Bend, port_count=2, required=True)
    # bend90: fp.IDevice = fp.DeviceParam(type=Bend90, port_count=2, required=True)

    # straight: fp.IDevice = fp.DeviceParam(type=Straight, port_count=2, required=False)

    def _default_waveguide_type(self):
        return get_technology().WG.CHANNEL.C.WIRE.updated(wg_design_width=self.Width)

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        Width = self.Width
        sHeight = self.sHeight
        sLength = self.sLength
        waveguide_type = self.waveguide_type
        port_names = self.port_names
        # bend = self.bend
        # bend90 = self.bend90
        # straight = self.straight

        if sHeight == sLength:
            bend_left = Bend90(Width=self.Width, Radius=self.sLength / 2, waveguide_type=self.waveguide_type)
            bend_right = Bend90(Width=self.Width, Radius=self.sLength / 2,
                                waveguide_type=self.waveguide_type).c_mirrored().translated(self.sLength, 0)

            insts += bend_left, bend_right

        if sHeight > sLength:
            bend_left = Bend90(Width=self.Width, Radius=self.sLength / 2, waveguide_type=self.waveguide_type)
            bend_right = Bend90(Width=self.Width, Radius=self.sLength / 2, waveguide_type=self.waveguide_type).c_mirrored().translated(self.sLength, -(self.sHeight - self.sLength))
            straight = StraightBetween(start=bend_left["op_0"].position, end=bend_right["op_0"].position, waveguide_type=self.waveguide_type)

            insts += bend_left, bend_right, straight

        if sHeight < sLength:
            x = self.sLength / 2
            y = self.sHeight / 2
            a = (x ** 2 - y ** 2)/ 2 / x
            radius = y + a
            print(a)
            angle = numpy.rad2deg(math.cos(a / (a + y)))
            bend_left = Bend(Radius=radius, StartAngle=angle, EndAngle=90, waveguide_type=self.waveguide_type)
            bend_right = bend_left.c_mirrored().translated(0, 2 * a)

            insts += bend_left, bend_right

        # ports += bend_left["op_1"].with_name(port_names[1])
        # ports += bend_right["op_1"].with_name(port_names[0])

        return insts, elems, ports


if __name__ == "__main__":
    from SITRI_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    library += Sbend(sHeight=5)

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
