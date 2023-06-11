from dataclasses import dataclass
from typing import Optional, Tuple, cast


from fnpcell import all as fp
from gpdk.components.bend.bend_circular import BendCircular
from gpdk.components.straight.straight import Straight
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class DCHalfRingStraight(fp.PCell):
    """
    Attributes:
        coupler_length: Length of the directional coupler
        coupler_spacing: Spacing between the two waveguide centre lines
        bend_radius: Bend radius for the auto-generated bends
        waveguide_type: type of waveguide
        port_names: defaults to ["op_0", "op_1", "op_2", "op_3"]

    Examples:
    ```python
    TECH = get_technology()
        dc = DirectionalCouplerBend(name="f", coupler_spacing=0.7, coupler_length=6, bend_radius=10, straight_after_bend=6, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(dc)
    ```
    ![DCHalfRingStraight](images/directional_coupler_half_ring.png)
    """

    coupler_length: float = fp.FloatParam(default=0, min=0, doc="Length of the directional coupler")
    coupler_spacing: float = fp.PositiveFloatParam(default=0.2, doc="Spacing between the two waveguide centre lines")
    bend_radius: Optional[float] = fp.PositiveFloatParam(default=10, doc="Bend radius for the auto-generated bends")
    waveguide_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType, doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4, default=["op_0", "op_1", "op_2", "op_3"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        # fmt: off
        coupler_length = self.coupler_length
        coupler_spacing = self.coupler_spacing
        bend_radius = self.bend_radius
        waveguide_type = self.waveguide_type
        port_names = self.port_names

        if bend_radius is None:
            bend_radius = cast(float, waveguide_type.BEND_CIRCULAR.radius_eff) # type: ignore

        width = waveguide_type.core_width
        bottom_waveguide_length = 2 * bend_radius + coupler_length + 3 * width

        left_bend = BendCircular(name="left_bend", radius=bend_radius, waveguide_type=waveguide_type).c_mirrored().translated(-coupler_length / 2, 0)
        bottom_waveguide = Straight(name="bottom_waveguide", length=bottom_waveguide_length, anchor=fp.Anchor.CENTER, waveguide_type=waveguide_type, transform=fp.translate(0, -bend_radius - coupler_spacing - width))
        right_bend = left_bend.h_mirrored()

        insts += left_bend
        ports += left_bend["op_0"].with_name(port_names[0])
        insts += bottom_waveguide
        ports += bottom_waveguide["op_0"].with_name(port_names[1])
        ports += bottom_waveguide["op_1"].with_name(port_names[2])
        insts += right_bend
        ports += right_bend["op_0"].with_name(port_names[3])
        coupler_straight = (
            Straight(
                name="coupler_straight",
                length=coupler_length,
                waveguide_type=waveguide_type,
                anchor=fp.Anchor.CENTER,
                transform=fp.translate(0, -bend_radius),
            )
            if coupler_length > 0
            else None
        )
        if not coupler_straight is None:
            insts += coupler_straight

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += DCHalfRingStraight()
    # library += DCHalfRingStraight(name="f", coupler_length=0, coupler_spacing=0.2, bend_radius=10,waveguide_type=TECH.WG.FWG.C.WIRE)
    # library += DCHalfRingStraight(name="s", coupler_length=1, coupler_spacing=0.2, bend_radius=10, waveguide_type=TECH.WG.SWG.C.WIRE)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
