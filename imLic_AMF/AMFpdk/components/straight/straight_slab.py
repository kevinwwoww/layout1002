from dataclasses import dataclass
from functools import cached_property
from typing import Tuple
from fnpcell import all as fp
from fnpcell.interfaces import angle_between, distance_between
from AMFpdk.technology import get_technology


@dataclass(eq=False)
class SlabStraight(fp.IWaveguideLike, fp.PCell):
    length: float = fp.FloatParam(default=10, min=0)
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_waveguide_type(self):
        return get_technology().WG.RIB.C.WIRE

    # @cached_property
    # def raw_curve(self):
    #     return fp.g.Line(
    #         length=self.length,
    #         anchor=self.anchor,
    #     )

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        length = self.length
        waveguide_type = self.waveguide_type
        port_names = self.port_names
        anchor = self.anchor
        height = TECH.WG.SLAB.C.wg_design_width

        wg = waveguide_type(
            curve=fp.g.Line(
                length=length,
                anchor=fp.Anchor.CENTER,
                origin=(0, 0,)
            ),
        ).with_name("rib_wg")
        insts += wg
        ports += wg["op_0"].with_name(port_names[0])
        ports += wg["op_1"].with_name(port_names[1])

        slab_layer = TECH.LAYER.SLAB
        height = 10
        slab_wg = fp.el.Rect(width=length, height=height, center=(0, 0), layer=slab_layer)
        elems += slab_wg

        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    library += SlabStraight(length=25)

    fp.export_gds(library, file=gds_file)
