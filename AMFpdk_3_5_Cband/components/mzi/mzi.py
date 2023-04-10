from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk.components.directional_coupler.directional_coupler import DirectionalCoupler
from AMFpdk.technology import get_technology, WG

@dataclass(eq=False)
class MZI(fp.PCell):
    length_difference: float = fp.PositiveFloatParam(default=100)
    coupler_spacing: float = fp.PositiveFloatParam(default=2)
    coupler_length: float = fp.PositiveFloatParam(default=6)
    bend_radius: float = fp.PositiveFloatParam(default=10)
    straight_after_bend: float = fp.PositiveFloatParam(default=5)
    x_between2dc: float = fp.PositiveFloatParam(default=100)
    waveguide_type: WG.RIB.C = fp.WaveguideTypeParam(type=WG.RIB.C)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4, default=["op_1", "op_2", "op_3", "op_4"])
    dc_left: fp.IDevice = fp.DeviceParam(type=DirectionalCoupler, port_count=4, required=False)
    dc_right: fp.IDevice = fp.DeviceParam(type=DirectionalCoupler, port_count=4, required=False)

    def _default_waveguide_type(self):
        return get_technology().WG.RIB.C.WIRE

    def _default_dc_left(self):
        return DirectionalCoupler(
            name="dc",
            coupler_spacing=self.coupler_spacing,
            coupler_length=self.coupler_length,
            bend_radius=self.bend_radius,
            straight_after_bend=self.straight_after_bend,
            waveguide_type=get_technology().WG.RIB.C.WIRE
        )

    def _default_dc_right(self):
        return DirectionalCoupler(
            name="dc",
            coupler_spacing=self.coupler_spacing,
            coupler_length=self.coupler_length,
            bend_radius=self.bend_radius,
            straight_after_bend=self.straight_after_bend,
            waveguide_type=get_technology().WG.RIB.C.WIRE,
            transform=fp.translate(self.x_between2dc, 0)
        )

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()

        length_difference = self.length_difference
        waveguide_type = self.waveguide_type
        port_names = self.port_names
        DC_left = self.dc_left
        DC_right = self.dc_right

        DC_left = DC_left
        DC_right = DC_right
        insts += DC_left
        insts += DC_right

        ports += DC_left["op_0"].with_name(port_names[0])
        ports += DC_left["op_1"].with_name(port_names[1])
        ports += DC_right["op_2"].with_name(port_names[2])
        ports += DC_right["op_3"].with_name(port_names[3])

        link_up = fp.create_links(
            link_type=get_technology().WG.RIB.C.WIRE,
            bend_factory=get_technology().WG.RIB.C.WIRE.BEND_CIRCULAR,
            specs=[
                DC_left["op_3"] >> DC_right["op_0"],
            ],

        )

        insts += link_up

        link_down = fp.create_links(
            link_type=get_technology().WG.RIB.C.WIRE,
            bend_factory=get_technology().WG.RIB.C.WIRE.BEND_CIRCULAR,
            specs=[
                fp.LinkBetween(
                    start=DC_left["op_2"],
                    end=DC_right["op_1"],
                    target_length=link_up[0].curve_length+length_difference,
                )
            ]
        )
        print(link_up[0].curve_length)
        print(link_down[0].curve_length)

        insts += link_down

        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")

    library = fp.Library()
    TECH = get_technology()

    library += MZI(length_difference=500)

    fp.export_gds(library, file=gds_file)
