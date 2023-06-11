#### import necessary modules ####

from dataclasses import dataclass, field
from typing import cast

from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology  # get TECH definition
from gpdk.technology.interfaces import CoreCladdingWaveguideType

#### finish import ####

#### define pcell, use RingResonator for example ####


# the dataclass decorator is for IDE code complete
@dataclass(eq=False)
class RingResonator(fp.PCell, band="C"):
    #
    # define parameters
    #
    # parameter，with default value 5, will be validated in __post_pcell_init__
    ring_radius: float = 5
    # parameter，positive，with default value 0.2
    top_spacing: float = fp.PositiveFloatParam(default=0.2)
    # parameter，positive，with default value 0.2
    bottom_spacing: float = fp.PositiveFloatParam(default=0.2)
    # parameter for waveguide，which contains core_width, core_layer, cladding_layer, bend_radius ...
    ring_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    top_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    bottom_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(
        type=CoreCladdingWaveguideType,
        # call default_factory after __post_init__ but before __post_pcell_init__
        # default_factory="_default_{name}", # if default_factory is function, it will be called directly. Otherwise method with the specific name will be called
    )
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4, default=["op_0", "op_1", "op_2", "op_3"])
    # finish parameter definition

    def _default_bottom_type(self):
        return get_technology().WG.FWG.C.WIRE

    def __post_pcell_init__(self):
        assert self.ring_radius > 0, "ring_radius must be > 0"
        # self.ring_radius = xxx is allowed here
        # outside this function, the instance is frozen

    def build(self):
        # create insts,elems,ports, fixed template
        insts, elems, ports = fp.InstanceSet(), fp.ElementSet(), fp.PortSet()
        # fmt: off

        # custom region start
        #
        min_radius_of_type = cast(float, self.ring_type.BEND_CIRCULAR.radius_eff)  # type: ignore

        ring = self.ring_type(curve=fp.g.EllipticalArc(radius=self.ring_radius)).with_ports((None, None)).with_name("ring")
        insts += ring
        ring_core_width = self.ring_type.core_width
        ring_cladding_width = self.ring_type.cladding_width

        line_length = self.ring_radius * 2 + ring_cladding_width

        top_core_width = self.top_type.core_width
        top = pdk.Straight(name="top", length=line_length, waveguide_type=self.top_type, transform=fp.translate(-line_length / 2, self.ring_radius + self.top_spacing + top_core_width / 2 + ring_core_width / 2))
        insts += top
        ports += top["op_0"].with_name(self.port_names[0])
        ports += top["op_1"].with_name(self.port_names[3])
        bottom_core_width = self.bottom_type.core_width
        bottom = pdk.Straight(name="bottom", length=line_length, waveguide_type=self.bottom_type, transform=fp.translate(-line_length / 2, -(self.ring_radius + self.bottom_spacing + bottom_core_width / 2 + ring_core_width / 2)))
        insts += bottom
        ports += bottom["op_0"].with_name(self.port_names[1])
        ports += bottom["op_1"].with_name(self.port_names[2])

        # custom region end
        # fmt: on
        return insts, elems, ports


@dataclass(eq=False)
class RingResonator2(RingResonator, band="C"):
    ring_radius: float = fp.PositiveFloatParam(default=10)
    computed_value: float = field(init=False)
    computed_v2: float = 7

    def _default_bottom_type(self):
        return get_technology().WG.SWG.C.WIRE

    def __post_pcell_init__(self):
        self.computed_value = self.ring_radius * 2
        self.computed_v2 = 8


if __name__ == "__main__":
    # fixed template start
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    # =============================================================
    # fmt: off
    # fixed template end
    # custom region start
    r0 = RingResonator(ring_radius=60, ring_type=TECH.WG.FWG.C.WIRE, top_type=TECH.WG.FWG.C.WIRE, bottom_type=TECH.WG.MWG.C.WIRE)
    library += r0
    r1 = RingResonator(ring_type=TECH.WG.FWG.C.WIRE, top_type=TECH.WG.FWG.C.WIRE).translated(20, 0)
    library += r1
    r2 = RingResonator2(ring_type=TECH.WG.FWG.C.WIRE, top_type=TECH.WG.FWG.C.WIRE).translated(50, 0)
    library += r2
    # custom region end

    # fixed template start
    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
    # fixed template end
