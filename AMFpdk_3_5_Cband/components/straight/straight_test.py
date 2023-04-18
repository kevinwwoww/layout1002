from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from fnpcell import all as fp
from fnpcell.interfaces import angle_between, distance_between
from AMFpdk_3_5_Cband.technology import get_technology, WG


@dataclass(eq=False)
class Straight1(fp.IWaveguideLike, fp.PCell):
    Length: float = fp.FloatParam(default=10, min=0)
    Width: float = fp.FloatParam(default=0.5, min=0)
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=("op_0", "op_1"))

    def _default_waveguide_type(self):
        return get_technology().WG.CHANNEL.C.WIRE
    

    def build(self):
        insts, elems, ports = super().build()

        length = self.Length
        width = self.Width
        waveguide_type = self.waveguide_type
        anchor = self.anchor
        port_names = self.port_names

        wg = fp.el.Line(
            length=length,
            stroke_width=width,
            anchor=anchor,
            layer=waveguide_type.wg_layer
        )

        elems += wg

        start, end = wg.end_rays
        ports += fp.Port(
            name=port_names[0],
            at=start,
            waveguide_type=waveguide_type
        )
        ports += fp.Port(
            name=port_names[1],
            at=end,
            waveguide_type=waveguide_type
        )
        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk_3_5_Cband.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += Straight1()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
