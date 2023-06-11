import numpy
from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.technology.waveguide_factory import EulerBendFactory


@dataclass(eq=False)
class QKD(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        dc_left = pdk.DirectionalCouplerSBend(coupler_spacing=0.7, coupler_length=10, bend_radius=15, bend_degrees=30, straight_after_bend=10)
        dc_right = pdk.DirectionalCouplerSBend(coupler_spacing=0.7, coupler_length=10, bend_radius=15, bend_degrees=30, straight_after_bend=10).translated(200, 0)
        straight = pdk.Straight(length=90).translated((dc_right["op_0"].position[0]-dc_left["op_3"].position[0]) / 2 - 20, dc_left["op_3"].position[1])
        heater = pdk.TiNHeaterwithep(waveguide_length=90, tin_length=60, contact_box_size=6, metal_box_size=10).translated((dc_right["op_1"].position[0]-dc_left["op_2"].position[0]) / 2 + 20, dc_left["op_2"].position[1])

        mzi = fp.Linked(
            link_type=TECH.WG.FWG.C.WIRE,
            links=[
                dc_left["op_2"] >> heater["op_0"],
                heater["op_1"] >> dc_right["op_1"],
                dc_left["op_3"] >> straight["op_0"],
                straight["op_1"] >> dc_right["op_0"],
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

        spiral = pdk.Spiral(min_straight=10, total_length=20000, n_o_loops=18, spacing=10, waveguide_type=TECH.WG.FWG.C.WIRE).h_mirrored()
        spiral_start_x = 1700
        spiral_spacing = 100
        spiral_length = 530

        spiral_1 = [spiral.translated(spiral_start_x, 400)]
        spiral_g1 = spiral_1[0]
        spiral_2 = [spiral.translated(spiral_start_x + spiral_length + spiral_spacing, 400),
                    spiral.translated(spiral_start_x + spiral_length*2 + spiral_spacing, 400)]
        spiral_g2 = fp.Linked(
            link_type=TECH.WG.FWG.C.EXPANDED,
            links=[
                spiral_2[0]["op_0"] >> fp.Waypoint(spiral_2[0]["op_0"].position[0] + spiral_length / 2, spiral_2[0]["op_0"].position[1] - 30, 0) >> spiral_2[1]["op_1"]
            ],
            ports=[spiral_2[0]["op_1"].with_name("op_1"),
                   spiral_2[1]["op_0"].with_name("op_0")],
        )
        spiral_4 = [
            spiral.translated(spiral_start_x + spiral_length * 3 + spiral_spacing * 2, 400),
            spiral.translated(spiral_start_x + spiral_length * 4 + spiral_spacing * 2, 400),
            spiral.translated(spiral_start_x + spiral_length * 5 + spiral_spacing * 2, 400),
            spiral.translated(spiral_start_x + spiral_length * 6 + spiral_spacing * 2, 400),
        ]
        spiral_g4 = fp.Linked(
            link_type=TECH.WG.FWG.C.EXPANDED,
            # bend_factory=bend_factory, # bend_factory,
            links=[
                spiral_4[0]["op_0"] >> fp.Waypoint(spiral_4[0]["op_0"].position[0] + spiral_length / 2, spiral_4[0]["op_0"].position[1] - 30, 0) >> spiral_4[1]["op_1"],
                spiral_4[1]["op_0"] >> fp.Waypoint(spiral_4[1]["op_0"].position[0] + spiral_length / 2, spiral_4[1]["op_0"].position[1] - 30, 0) >> spiral_4[2]["op_1"],
                spiral_4[2]["op_0"] >> fp.Waypoint(spiral_4[2]["op_0"].position[0] + spiral_length / 2, spiral_4[2]["op_0"].position[1] - 30, 0) >> spiral_4[3]["op_1"],
            ],
            ports=[spiral_4[0]["op_1"].with_name("op_1"),
                   spiral_4[3]["op_0"].with_name("op_0"),
                   ],
        )
        mzi_start_x = spiral_start_x - spiral_length / 2
        mzi_1 = mzi
        mzi_2 = mzi.translated(600, (spiral_1[0]["op_1"].position[1] - mzi_1["op_3"].position[1]) / 2 - 25)
        mzi_3 = mzi.translated(1200, spiral_1[0]["op_1"].position[1] - mzi_1["op_3"].position[1] - 50)
        mzi_4 = mzi.translated(spiral_g2["op_1"].position[0] - 300, mzi_3["op_3"].position[1] - mzi_1["op_3"].position[1])
        mzi_5 = mzi.translated(spiral_g4["op_1"].position[0] - 300, mzi_3["op_3"].position[1] - mzi_1["op_3"].position[1])
        mzi_6 = mzi.translated(spiral_g4["op_1"].position[0] + 1800, mzi_3["op_3"].position[1] - mzi_1["op_3"].position[1])
        DC = dc_left.translated(mzi_6["op_2"].position[0] + 200, mzi_6["op_2"].position[1] - mzi_1["op_3"].position[1])

        TOPS = pdk.TiNHeaterwithep(waveguide_length=90, tin_length=80, tin_box_size=5, contact_box_size=2, metal_box_size=2).translated(spiral_g2["op_1"].position[0] + spiral_spacing / 2, DC["op_1"].position[1])
        # device edges (hotizontal distance 6300um, vertical distance 80um)
        edge_straight = pdk.Straight(length=90)
        edge_left = [
            edge_straight.translated(-400, -20),
            edge_straight.translated(-400, 60),
            edge_straight.translated(-400, 140),
            edge_straight.translated(-400, 220),
        ]
        edge_right = [
            edge_straight.translated(5900, mzi_1["op_2"].position[1]),
            edge_straight.translated(5900, 60),
            edge_straight.translated(5900, DC["op_3"].position[1]),
            edge_straight.translated(5900, 220),
        ]
        link_edge = [
            edge_left[0]["op_1"] >> mzi_1["op_1"],
            edge_left[1]["op_1"] >> mzi_1["op_0"],
            edge_left[2]["op_1"] >> mzi_2["op_0"],
            edge_left[3]["op_1"] >> mzi_3["op_0"],
            mzi_1["op_2"] >> edge_right[0]["op_0"],
            DC["op_2"] >> edge_right[1]["op_0"],
            DC["op_3"] >> edge_right[2]["op_0"],
            mzi_6["op_3"] >> fp.Waypoint(5500, 180, 90) >> edge_right[3]
            ["op_0"],
        ]
        BP = []
        BP_num = 14
        BP_x = numpy.linspace(-100, 5400, BP_num)
        for i in range(BP_num):
            BP.append(pdk.BondPad(pad_width=75,
                                  pad_height=75).translated(BP_x[i], -200))
        link_op = [mzi_1["op_3"] >> mzi_2["op_1"],
                   mzi_2["op_3"] >> mzi_3["op_1"],
                   mzi_3["op_2"] >> mzi_4["op_1"],
                   mzi_3["op_3"] >> spiral_g1["op_1"],
                   spiral_g1["op_0"] >> mzi_4["op_0"],
                   mzi_4["op_2"] >> mzi_5["op_1"],
                   mzi_4["op_3"] >> spiral_g2["op_1"],
                   spiral_g2["op_0"] >> mzi_5["op_0"],
                   mzi_5["op_2"] >> mzi_6["op_1"],
                   mzi_5["op_3"] >> spiral_g4["op_1"],
                   spiral_g4["op_0"] >> mzi_6["op_0"],
                   mzi_6["op_2"] >> DC["op_0"],
                   mzi_2["op_2"] >> TOPS["op_0"],
                   TOPS["op_1"] >> DC["op_1"]]
        link_ep = [mzi_1["ep_0"].with_orientation(degrees=-90) >> BP[0]["ep_0"].with_orientation(degrees=90).with_orientation(degrees=90),
                   mzi_1["ep_1"].with_orientation(degrees=-90) >> fp.Waypoint(BP_x[1], -70, 0) >> BP[1]["ep_0"].with_orientation(degrees=90),
                   mzi_2["ep_0"].with_orientation(degrees=-90) >> fp.Waypoint(BP_x[2], -90, 0) >> BP[2]["ep_0"].with_orientation(degrees=90),
                   mzi_2["ep_1"].with_orientation(degrees=-90) >> fp.Waypoint(BP_x[3], -70, 0) >> BP[3]["ep_0"].with_orientation(degrees=90),
                   mzi_3["ep_0"].with_orientation(degrees=-90) >> fp.Waypoint(BP_x[4], -100, 0) >> BP[4]["ep_0"].with_orientation(degrees=90),
                   mzi_3["ep_1"].with_orientation(degrees=-90) >> fp.Waypoint(BP_x[5], -95, 0) >> BP[5]["ep_0"].with_orientation(degrees=90),
                   mzi_4["ep_0"].with_orientation(degrees=-90) >> fp.Waypoint(BP_x[6], -90, 0) >> BP[6]["ep_0"].with_orientation(degrees=90),
                   mzi_4["ep_1"].with_orientation(degrees=-90) >> fp.Waypoint(BP_x[7], -85, 0) >> BP[7]["ep_0"].with_orientation(degrees=90),
                   TOPS["ep_0"].with_orientation(degrees=-90)  >> fp.Waypoint(BP_x[8], -70, 0) >> BP[8]["ep_0"].with_orientation(degrees=90),
                   TOPS["ep_1"].with_orientation(degrees=-90)  >> fp.Waypoint(BP_x[9], -60, 0) >> BP[9]["ep_0"].with_orientation(degrees=90),
                   mzi_5["ep_0"].with_orientation(degrees=-90) >> fp.Waypoint(BP_x[10], -50, 0) >> BP[10]["ep_0"].with_orientation(degrees=90),
                   mzi_5["ep_1"].with_orientation(degrees=-90) >> fp.Waypoint(BP_x[11], -40, 0) >> BP[11]["ep_0"].with_orientation(degrees=90),
                   mzi_6["ep_0"].with_orientation(degrees=-90) >> fp.Waypoint(BP_x[12], -70, 0) >> BP[12]["ep_0"].with_orientation(degrees=90),
                   mzi_6["ep_1"].with_orientation(degrees=-90) >> fp.Waypoint(BP_x[13], -70, 0) >> BP[13]["ep_0"].with_orientation(degrees=90),
                   ]
        link_device = fp.Linked(
            link_type=TECH.WG.FWG.C.EXPANDED,
            metal_line_type=TECH.METAL.M2.W20.updated(line_width=2),
            metal_min_distance=50,
            links=link_op + link_ep + link_edge,
            ports=[
                edge_left[3]["op_0"].with_name("op_0"),
                edge_left[2]["op_0"].with_name("op_1"),
                edge_left[1]["op_0"].with_name("op_2"),
                edge_left[0]["op_0"].with_name("op_3"),
                edge_right[0]["op_1"].with_name("op_4"),
                edge_right[1]["op_1"].with_name("op_5"),
                edge_right[2]["op_1"].with_name("op_6"),
                edge_right[3]["op_1"].with_name("op_7"),
            ],
        )
        insts += link_device

        return insts, elems, ports





if __name__ == "__main__":
        from pathlib import Path
        gds_file = Path(__file__).parent / "local" /Path(__file__).with_suffix(".gds").name
        library = fp.Library()
        TECH = get_technology()
        # =============================================================
        # fmt: off
        library += QKD()
        # fmt: on
        # =============================================================
        fp.export_gds(library, file=gds_file)


        # fp.plot(library)

