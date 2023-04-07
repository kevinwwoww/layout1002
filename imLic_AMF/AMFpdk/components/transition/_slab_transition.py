from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk.technology import WG
from AMFpdk.technology.interfaces import CoreWaveguideType

@dataclass(eq=False)
class SLABtransition(fp.PCell):
    length: float = fp.PositiveFloatParam(default=20, doc="Length of transition")
    wire_only_length: float = fp.PositiveFloatParam(default=5.0, doc="Length of transition where shallow part is built up")
    deep_only_width: float = fp.PositiveFloatParam(default=3.0, doc="Core width of the waveguide at the end of shallow transition part")
    slab_type: WG.SLAB.C = fp.WaveguideTypeParam(type=WG.SLAB.C)
    other_type: CoreWaveguideType = fp.WaveguideTypeParam()
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1", "op_2", "op_3"])

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        length = self.length
        wire_only_length = self.wire_only_length
        deep_only_width = self.deep_only_width
        slab_type = self.slab_type
        other_type = self.other_type
        anchor = self.anchor
        port_names = self.port_names

        slab_layer = slab_type.wg_layer
        slab_width = slab_type.wg_width

        other_layer = other_type.wg_layer
        other_width = other_type.wg_width

        tx = 0
        if anchor == fp.Anchor.END:
            tx = -length
        elif anchor == fp.Anchor.CENTER:
            tx = -length / 2
        transform = fp.translate(tx, 0)
        other = fp.el.Line(
            length=length,
            stroke_width=slab_width,
            final_stroke_width=other_width,
            layer=other_layer,
            transform=transform,
        )
        elems += other

        slab = fp.el.Line(
            length=wire_only_length,
            stroke_width=slab_width,
            final_stroke_width=deep_only_width,
            layer=slab_layer,
            transform=transform,
        )
        elems += slab

        start_ray, end_ray = other.end_rays
        ports += fp.Port(
            name=port_names[0],
            at= start_ray,
            waveguide_type=slab_type,
        )
        ports += fp.Port(
            name=port_names[1],
            at=end_ray,
            waveguide_type=other_type,
        )
        return insts, elems, ports

