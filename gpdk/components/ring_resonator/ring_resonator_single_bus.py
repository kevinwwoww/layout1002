from dataclasses import dataclass
from typing import Tuple, cast

from fnpcell import all as fp
from gpdk.components.straight.straight import Straight
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class RingResonatorSingleBus(fp.PCell):
    """
    Attributes:
        ring_radius: defaults to 5, Radius of the ring
        top_spacing: defaults to 0.2, Spacing between top and ring waveguides
        bottom_spacing: defaults to 0.2, Spacing between ring and bottom waveguides
        ring_type: type of waveguide of ring
        bottom_type: type of waveguide of bottom bus
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
        ring = RingResonatorSingleBus(ring_type=TECH.WG.FWG.C.WIRE, bottom_type=TECH.WG.FWG.C.WIRE)
    fp.plot(ring)
    ```
    ![RingResonatorSingleBus](images/ring_resonator_single_bus.png)
    """

    ring_radius: float = fp.PositiveFloatParam(default=5, doc="Radius of the ring")
    bottom_spacing: float = fp.PositiveFloatParam(default=0.2, doc="Spacing between ring and bottom waveguides")
    ring_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    bottom_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_ring_type(self):
        return get_technology().WG.FWG.C.WIRE

    def _default_bottom_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        # fmt: off
        ring_radius = self.ring_radius
        bottom_spacing = self.bottom_spacing
        ring_type = self.ring_type
        bottom_type = self.bottom_type
        port_names = self.port_names

        min_radius_of_type = cast(float, ring_type.BEND_CIRCULAR.radius_eff)  # type: ignore
        assert ring_radius >= min_radius_of_type

        ring = ring_type(curve=fp.g.EllipticalArc(radius=ring_radius)).with_ports((None, None)).with_name("ring")

        ring_core_width = ring_type.core_width
        ring_cladding_width = ring_type.cladding_width

        line_length = ring_radius * 2 + ring_cladding_width

        bottom_core_width = bottom_type.core_width
        insts += ring.translated(0, (ring_radius + bottom_spacing + bottom_core_width / 2 + ring_core_width / 2))
        bottom = Straight(name="bottom", length=line_length, anchor=fp.Anchor.CENTER, waveguide_type=bottom_type)
        insts += bottom
        ports += bottom["op_0"].with_name(port_names[0])
        ports += bottom["op_1"].with_name(port_names[1])

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += RingResonatorSingleBus(ring_type=TECH.WG.FWG.C.WIRE, bottom_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
