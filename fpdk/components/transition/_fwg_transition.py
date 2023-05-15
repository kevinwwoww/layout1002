from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from fpdk.technology import WG
from fpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class FWGTransition(fp.PCell):
    length: float = fp.PositiveFloatParam(default=20, doc="Length of transition")
    wire_only_length: float = fp.PositiveFloatParam(default=5.0, doc="Length of transition where shallow part is built up")
    deep_only_width: float = fp.PositiveFloatParam(default=3.0, doc="Core width of the waveguide at the end of shallow transition part")
    fwg_type: WG.FWG.C = fp.WaveguideTypeParam(type=WG.FWG.C)
    other_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam()
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1", "op_2", "op_3"])

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        length = self.length
        wire_only_length = self.wire_only_length
        deep_only_width = self.deep_only_width
        fwg_type = self.fwg_type
        other_type = self.other_type
        anchor = self.anchor
        port_names = self.port_names
        deep_only_width = deep_only_width + fwg_type.core_bias(deep_only_width)  # is this right ?

        fwg_core_layer = fwg_type.core_layer
        fwg_core_width = fwg_type.core_width
        fwg_cladding_layer = fwg_type.cladding_layer
        fwg_cladding_width = fwg_type.cladding_width

        other_core_layer = other_type.core_layer
        other_core_width = other_type.core_width
        other_cladding_layer = other_type.cladding_layer
        other_cladding_width = other_type.cladding_width

        tx = 0
        if anchor == fp.Anchor.END:
            tx = -length
        elif anchor == fp.Anchor.CENTER:
            tx = -length / 2
        transform = fp.translate(tx, 0)
        other_core = fp.el.Line(
            length=length,
            stroke_width=fwg_core_width,
            final_stroke_width=other_core_width,
            layer=other_core_layer,
            transform=transform,
        )
        elems += other_core
        other_cladding = fp.el.Line(
            length=length,
            stroke_width=fwg_cladding_width,
            final_stroke_width=other_cladding_width,
            end_hints=((fwg_core_width / 2, -fwg_core_width / 2), (other_core_width / 2, -other_core_width / 2)),
            layer=other_cladding_layer,
            transform=transform,
        )
        elems += other_cladding

        fwg_core = fp.el.Line(
            length=wire_only_length,
            stroke_width=fwg_core_width,
            final_stroke_width=deep_only_width,
            layer=fwg_core_layer,
            transform=transform,
        )
        elems += fwg_core
        fwg_cladding = fp.el.Line(
            length=wire_only_length,
            stroke_width=fwg_cladding_width,
            final_stroke_width=fwg_cladding_width - fwg_core_width + deep_only_width,
            end_hints=((fwg_core_width / 2, -fwg_core_width / 2), (deep_only_width / 2, -deep_only_width / 2)),
            layer=fwg_cladding_layer,
            transform=transform,
        )
        elems += fwg_cladding

        start_ray, end_ray = other_core.end_rays
        ports += fp.Port(
            name=port_names[0],
            at=start_ray,
            waveguide_type=fwg_type,
        )
        ports += fp.Port(
            name=port_names[1],
            at=end_ray,
            waveguide_type=other_type,
        )
        return insts, elems, ports

    # return FWGTransition
