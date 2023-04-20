from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk_3_5_Cband.technology import WG, get_technology
from AMFpdk_3_5_Cband.technology.interfaces import CoreWaveguideType


@dataclass(eq=False)
class SLAB2RIBtransition(fp.PCell):
    Length: float = fp.PositiveFloatParam(default=10.0, doc="Length of transition")
    Width: float = fp.PositiveFloatParam(default=0.5, doc="Length of transition")
    leftWidth: float = fp.PositiveFloatParam(default=0.3, doc="Length of transition")
    rightWidth: float = fp.PositiveFloatParam(default=5.0, doc="Length of transition")
    rib_type: fp.IWaveguideType = fp.WaveguideTypeParam(type=WG.CHANNEL.C)
    slab_type: fp.IWaveguideType = fp.WaveguideTypeParam(type=WG.SLAB.C)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_rib_type(self):
        return get_technology().WG.CHANNEL.C.WIRE

    def _default_slab_type(self):
        return get_technology().WG.SLAB.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        length = self.Length
        width = self.Width
        leftwidth = self.leftWidth
        rightwidth = self.rightWidth
        # wire_only_length = self.wire_only_length
        # deep_only_width = self.deep_only_width
        rib_type = self.rib_type
        slab_type = self.slab_type
        anchor = self.anchor
        port_names = self.port_names

        rib_layer = rib_type.wg_layer
        # rib_width = rib_type.wg_width

        slab_layer = slab_type.wg_slab_layer
        # slab_width = slab_layer.wg_rib_width

        tx = 0
        if anchor == fp.Anchor.END:
            tx = -length
        elif anchor == fp.Anchor.CENTER:
            tx = -length / 2
        transform = fp.translate(tx, 0)
        slab = fp.el.Line(
            length=length,
            stroke_width=leftwidth,
            final_stroke_width=rightwidth,
            layer=slab_layer,
            # transform=transform,
        )
        elems += slab

        rib = fp.el.Line(
            length=length,
            stroke_width=width,
            final_stroke_width=width,
            layer=rib_layer,
            # transform=transform,
        )
        elems += rib

        start_ray, end_ray = slab.end_rays
        ports += fp.Port(
            name=port_names[0],
            at=start_ray,
            waveguide_type=rib_type,
        )
        ports += fp.Port(
            name=port_names[1],
            at=end_ray,
            waveguide_type=slab_type,
        )
        return insts, elems, ports




if __name__ == "__main__":
    from AMFpdk_3_5_Cband.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    # library += SLAB2RIBtransition(rib_type=TECH.WG.CHANNEL.C.WIRE, slab_type=TECH.WG.SLAB.C.WIRE)
    library += SLAB2RIBtransition()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
