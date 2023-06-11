import math
from dataclasses import dataclass
from typing import Optional, Tuple, cast
from fnpcell import all as fp
from gpdk.components.sbend.sbend_circular import SBendCircular
from gpdk.components.straight.straight import Straight
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class DirectionalCouplerSBend(fp.PCell):
    """
    Attributes:
        coupler_spacing: Spacing between the two waveguide centre lines.
        coupler_length: Length of the directional coupler
        bend_radius: Bend radius for the auto-generated bends
        bend_degrees: Angle(in degrees) at which the directional coupler is bent
        straight_after_bend: Length of the straight waveguide after the bend
        waveguide_type: type of waveguide
        port_names: defaults to ["op_0", "op_1", "op_2", "op_3"]

    Examples:
    ```python
    TECH = get_technology()
        dc = DirectionalCouplerSBend(name="f", coupler_spacing=0.7, coupler_length=6, bend_radius=10, bend_degrees=30, straight_after_bend=6, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(dc)
    ```
    ![DirectionalCouplerSBend](images/directional_coupler_sbend.png)
    """

    coupler_spacing: float = fp.PositiveFloatParam(default=0.7, doc="Spacing between the two waveguide centre lines.")
    coupler_length: float = fp.PositiveFloatParam(default=6, doc="Length of the directional coupler")
    bend_radius: Optional[float] = fp.PositiveFloatParam(required=False, doc="Bend radius for the auto-generated bends")
    bend_degrees: float = fp.DegreeParam(default=30, min=0, max=90, invalid=[0], doc="Angle(in degrees) at which the directional coupler is bent")
    straight_after_bend: float = fp.PositiveFloatParam(default=6, doc="Length of the straight waveguide after the bend")
    waveguide_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType, doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4, default=["op_0", "op_1", "op_2", "op_3"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()

        coupler_spacing = self.coupler_spacing
        coupler_length = self.coupler_length
        bend_radius = self.bend_radius
        bend_degrees = self.bend_degrees
        straight_after_bend = self.straight_after_bend
        waveguide_type = self.waveguide_type
        port_names = self.port_names

        if bend_radius is None:
            bend_radius = cast(float, waveguide_type.BEND_CIRCULAR.radius_eff)  # type: ignore

        assert coupler_spacing > waveguide_type.core_width, "waveguide core overlap: coupler spacing must be greater than core_width"

        central_angle = math.radians(bend_degrees)
        d = bend_radius * math.sin(central_angle)
        h = bend_radius - bend_radius * math.cos(central_angle)
        sbend_height = h * 2
        sbend_distance = d * 2

        dy = coupler_spacing / 2
        dx = coupler_length / 2

        right_straight_after_bend = Straight(
            name="afterbend",
            length=straight_after_bend,
            waveguide_type=waveguide_type,
            transform=fp.translate(dx + sbend_distance, -dy - sbend_height),
        )
        left_straight_after_bend = right_straight_after_bend.h_mirrored()
        sbend = SBendCircular(
            name="sbend",
            distance=sbend_distance,
            height=sbend_height,
            min_radius=bend_radius,
            waveguide_type=waveguide_type,
            transform=fp.translate(-d - dx, -h - dy),
        )
        straight_coupler = Straight(
            name="coupler",
            length=coupler_length,
            waveguide_type=waveguide_type,
            transform=fp.translate(-dx, -dy),
        )

        bottom_half = fp.Device(
            name="bottom",
            content=[
                right_straight_after_bend,
                sbend,
                straight_coupler,
                sbend.h_mirrored(),
                left_straight_after_bend,
            ],
            ports=[
                left_straight_after_bend["op_1"].with_name("op_0"),
                right_straight_after_bend["op_1"],
            ],
        )
        insts += bottom_half
        # ports += bottom_half["op_0"].with_name(port_names[1])  # for right port index(0 1 2 3) in netlist
        # ports += bottom_half["op_1"].with_name(port_names[2])
        top_half = bottom_half.v_mirrored()
        insts += top_half
        ports += top_half["op_0"].with_name(port_names[0])
        ports += bottom_half["op_0"].with_name(port_names[1])
        ports += bottom_half["op_1"].with_name(port_names[2])
        ports += top_half["op_1"].with_name(port_names[3])

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += DirectionalCouplerSBend()
    # library += DirectionalCouplerSBend(name="f", coupler_spacing=0.7, coupler_length=6, bend_radius=10, bend_degrees=30, straight_after_bend=6, waveguide_type=TECH.WG.FWG.C.WIRE)
    # library += DirectionalCouplerSBend(name="s", coupler_spacing=1.7, coupler_length=6, bend_radius=20, bend_degrees=30, straight_after_bend=6, waveguide_type=TECH.WG.SWG.C.WIRE)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
