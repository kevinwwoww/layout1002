from dataclasses import dataclass
from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk import all as pdk

@dataclass(eq=False)
class MZI(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        dc_left = pdk.DirectionalCouplerSBend(coupler_spacing=0.7, coupler_length=10, bend_radius=15, bend_degrees=30,
                                              straight_after_bend=10)
        dc_right = pdk.DirectionalCouplerSBend(coupler_spacing=0.7, coupler_length=10, bend_radius=15, bend_degrees=30,
                                               straight_after_bend=10).translated(100, 0)
        heater = pdk.TiNHeaterwithep(waveguide_length=10, tin_length=40, contact_box_size=6, metal_box_size=10).translated((dc_right["op_1"].position[0]+dc_left["op_2"].position[0]) / 2 , dc_left["op_2"].position[1])

        # straight = pdk.Straight(length=90).translated(
        #     (dc_right["op_0"].position[0] - dc_left["op_3"].position[0]) / 2 - 20, dc_left["op_3"].position[1])

        mzi = fp.Linked(
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.EXPANDED,
            links=[
                dc_left["op_2"] >> heater["op_0"],
                heater["op_1"] >> dc_right["op_1"],
                dc_left["op_3"] >> dc_right["op_0"],
            ],
            ports=[
                dc_left["op_0"].with_name("op_0"),
                dc_left["op_1"].with_name("op_1"),
                dc_right["op_2"].with_name("op_2"),
                dc_right["op_3"].with_name("op_3"),
                heater["ep_0"].with_name("ep_0"),
                heater["ep_1"].with_name("ep_1"),
            ],
        )
        # print(dc_left.ports)


        insts += mzi
        return insts, elems, ports

if __name__ == "__main__":
    from pathlib import Path
    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    library = fp.Library()
    TECH = get_technology()

    library += MZI()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)

