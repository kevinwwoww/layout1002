from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk_3_5_Cband.technology import WG
from AMFpdk_3_5_Cband.technology.interfaces import CoreWaveguideType

@dataclass(eq=False)
class RIBtransition(fp.PCell):
    length: float = fp.PositiveFloatParam(default=20, doc="Length of transition")
    wire_only_length: float = fp.PositiveFloatParam(default=5.0, doc="Length of transition where shallow part is built up")
    deep_only_width: float = fp.PositiveFloatParam(default=3.0, doc="Core width of the waveguide at the end of shallow transition part")
    rib_type: WG.RIB.C = fp.WaveguideTypeParam(type=WG.RIB.C)
    other_type: CoreWaveguideType = fp.WaveguideTypeParam()
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1", "op_2", "op_3"])

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        length = self.length
        wire_only_length = self.wire_only_length
        deep_only_width = self.deep_only_width
        rib_type = self.rib_type
        other_type = self.other_type
        anchor = self.anchor
        port_names = self.port_names

        rib_layer = rib_type.wg_layer
        rib_width = rib_type.wg_width

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
            stroke_width=rib_width,
            final_stroke_width=other_width,
            layer=other_layer,
            transform=transform,
        )
        elems += other

        rib = fp.el.Line(
            length=wire_only_length,
            stroke_width=rib_width,
            final_stroke_width=deep_only_width,
            layer=rib_layer,
            transform=transform,
        )
        elems += rib

        start_ray, end_ray = other.end_rays
        ports += fp.Port(
            name=port_names[0],
            at= start_ray,
            waveguide_type=rib_type,
        )
        ports += fp.Port(
            name=port_names[1],
            at=end_ray,
            waveguide_type=other_type,
        )
        return insts, elems, ports

