from dataclasses import dataclass
from typing import Tuple, cast
from fnpcell import all as fp
from AMFpdk.components.bend.bend_circular import BendCircular
from AMFpdk.components.straight.straight import Straight
from AMFpdk.technology import get_technology
from AMFpdk.technology.interfaces import CoreWaveguideType

@dataclass(eq=False)
class DirectionalCoupler(fp.PCell):
    coupler_spacing: float = fp.PositiveFloatParam(default=0.7, doc="Coupler spacing, set by AMF device manual")
    coupler_length: float = fp.PositiveFloatParam(default=5, doc="Length of the directional coupler")
    bend_radius: float = fp.PositiveFloatParam(required=False, doc="Bend radius of the auto-generated bends")
    straight_after_bend: float = fp.PositiveFloatParam(default=3, doc="Length of the straight waveguide after the bends")
    waveguide_type: CoreWaveguideType = fp.WaveguideTypeParam(type=CoreWaveguideType, doc="Waveguide Type of the DC")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4, default=["op_0", "op_1","op_2","op_3",])

    def _default_waveguide_type(self):
        return get_technology().WG.RIB.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()

        coupler_spacing = self.coupler_spacing
        coupler_length = self.coupler_length
        bend_radius = self.bend_radius
        straight_after_bend = self.straight_after_bend
        waveguide_type = self.waveguide_type
        port_names = self.port_names

        if bend_radius is None:
            bend_radius = cast(float, waveguide_type.BEND_CIRCULAR.radius_eff)

        assert (
            coupler_spacing > waveguide_type.wg_width
        ),"waveguide core overlap: coupler spacing must be greater than wg_width"

        dy = coupler_spacing / 2

        left_straight_after_bend = Straight(name="leftafterbend", length=straight_after_bend, waveguide_type=waveguide_type)
        right_straight_after_bend = Straight(name="rightafterbend", length=straight_after_bend,
                                            waveguide_type=waveguide_type)
        left_bend = BendCircular(name="leftbend", degrees=90, radius=bend_radius, waveguide_type=waveguide_type)
        right_bend = BendCircular(name="rightbend", degrees=90, radius=bend_radius, waveguide_type=waveguide_type)
        straight_coupler = Straight(name="coupler", length=coupler_length, anchor=fp.Anchor.CENTER, waveguide_type=waveguide_type, transform=fp.translate(0, -dy))

        bottom_half = fp.Connected(
            name="bottom",
            joints=[
                straight_coupler["op_0"] <= left_bend["op_0"],
                left_bend["op_1"] <= left_straight_after_bend["op_1"],

                straight_coupler["op_1"] <= right_bend["op_1"],
                right_bend["op_0"] <= right_straight_after_bend["op_0"],
            ],
            ports=[
                left_straight_after_bend["op_0"],
                right_straight_after_bend["op_1"],
            ]
        )
        insts += bottom_half
        top_half = bottom_half.rotated(degrees=180)
        insts += top_half
        ports += top_half["op_1"].with_name(port_names[0]),
        ports += bottom_half["op_0"].with_name(port_names[1]),
        ports += bottom_half["op_1"].with_name(port_names[2]),
        ports += top_half["op_0"].with_name(port_names[3]),

        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file
    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += DirectionalCoupler()

    fp.export_gds(library, file=gds_file)