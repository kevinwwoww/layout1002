from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk.technology import WG
from AMFpdk.technology.interfaces import CoreWaveguideType, SlabWaveguideType

@dataclass(eq=False)
class CHANNELtransition(fp.PCell):
    length: float = fp.PositiveFloatParam(default=20, doc="Length of transition")
    wire_only_length: float = fp.PositiveFloatParam(default=5.0, doc="Length of transition where shallow part is built up")
    deep_only_width: float = fp.PositiveFloatParam(default=3.0, doc="Core width of the waveguide at the end of shallow transition part")
    channel_type: WG.CHANNEL.C = fp.WaveguideTypeParam(type=WG.CHANNEL.C)
    rib_type: SlabWaveguideType = fp.WaveguideTypeParam()
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1", "op_2", "op_3"])

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        length = self.length
        wire_only_length = self.wire_only_length
        deep_only_width = self.deep_only_width
        channel_type = self.channel_type
        rib_type = self.rib_type
        anchor = self.anchor
        port_names = self.port_names

        channel_layer = channel_type.wg_layer
        channel_width = channel_type.wg_width

        other_layer = rib_type.wg_layer
        other_width = rib_type.wg_layout_width

        tx = 0
        if anchor == fp.Anchor.END:
            tx = -length
        elif anchor == fp.Anchor.CENTER:
            tx = -length / 2
        transform = fp.translate(tx, 0)
        other = fp.el.Line(
            length=length,
            stroke_width=channel_width,
            final_stroke_width=other_width,
            layer=other_layer,
            transform=transform,
        )
        elems += other

        channel = fp.el.Line(
            length=wire_only_length,
            stroke_width=channel_width,
            final_stroke_width=deep_only_width,
            layer=channel_layer,
            transform=transform,
        )
        elems += channel

        start_ray, end_ray = other.end_rays
        ports += fp.Port(
            name=port_names[0],
            at= start_ray,
            waveguide_type=channel_type,
        )
        ports += fp.Port(
            name=port_names[1],
            at=end_ray,
            waveguide_type=rib_type,
        )
        return insts, elems, ports

