from dataclasses import dataclass
from typing import Optional, Tuple ,cast
from fnpcell import all as fp
from AMFpdk.components.straight.straight import Straight
from AMFpdk.technology import get_technology
from AMFpdk.technology.interfaces import CoreWaveguideType

@dataclass(eq=False)
class RingResonator(fp.PCell):
    ring_radius: float = fp.PositiveFloatParam(default=10, doc="Ring Radius")
    top_spacing: float = fp.PositiveFloatParam(default=0.2, doc="Spacing btn top WG and Ring")
    bottom_spacing: float = fp.PositiveFloatParam(default=0.2, doc="Spacing btn bottom WG and Ring")
    ring_type: CoreWaveguideType = fp.WaveguideTypeParam(type=CoreWaveguideType)
    top_type: Optional[CoreWaveguideType] = fp.WaveguideTypeParam(type=CoreWaveguideType, required=False)
    bottom_type: Optional[CoreWaveguideType] = fp.WaveguideTypeParam(type=CoreWaveguideType, required=False)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4, default=["op_0", "op_1", "op_2", "op_3"])

    def _default_ring_type(self):
        return get_technology().WG.RIB.C.WIRE

    def _default_top_type(self):
        return get_technology().WG.RIB.C.WIRE

    def _default_bottom_type(self):
        return get_technology().WG.RIB.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()

        ring_radius = self.ring_radius
        top_spacing = self.top_spacing
        bottom_spacing = self.bottom_spacing
        ring_type = self.ring_type
        top_type = self.top_type
        bottom_type = self.bottom_type
        port_names = self.port_names

        if top_type is None:
            top_type = ring_type
        if bottom_type is None:
            bottom_type = ring_type

        min_radius_of_type = cast(float, ring_type.BEND_CIRCULAR.radius_eff)

        assert ring_radius >= min_radius_of_type

        ring = ring_type(fp.g.EllipticalArc(radius=ring_radius)).with_ports((None, None)).with_name("ring")
        insts += ring
        ring_wg_width = ring_type.wg_width

        line_length = ring_radius * 2

        top_wg_width = top_type.wg_width
        top = Straight(name="top", length=line_length, waveguide_type=top_type, transform=fp.translate(-line_length / 2, ring_radius + top_spacing + top_wg_width / 2 + ring_wg_width / 2))
        insts += top
        ports += top["op_0"].with_name(port_names[0])
        ports += top["op_1"].with_name(port_names[3])

        bottom_wg_width = bottom_type.wg_width
        bottom = Straight(name="bottom", length=line_length, waveguide_type=top_type, transform=fp.translate(-line_length / 2,
                                                                                                       -(ring_radius + top_spacing + top_wg_width / 2 + ring_wg_width / 2)))
        insts += bottom
        ports += bottom["op_0"].with_name(port_names[1])
        ports += bottom["op_1"].with_name(port_names[2])

        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file
    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()
    library += RingResonator()
    fp.export_gds(library, file=gds_file)
    fp.plot(library)

