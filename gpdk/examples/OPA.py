from dataclasses import dataclass
from typing import Mapping, cast

import numpy
import numpy as np
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.components.step.step2.mmi1x2 import MMI1x2


@dataclass(eq=False)
class MMITree(fp.PCell):
    x_spacing: float = fp.PositiveFloatParam(default=50)
    end_y_spacing: float = fp.PositiveFloatParam(default=100)
    order: float = fp.PositiveFloatParam(default=3)
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        x_spacing = self.x_spacing
        end_y_spacing = self.end_y_spacing
        order = self.order
        mmi = MMI1x2()
        num_per_col = []
        v_spacing = []

        for i in range(order):
            num_per_col.append(2**i)
            v_spacing.append(end_y_spacing*(2**(order - i - 1)))

        for i in range(order):
            for j in range(num_per_col[i]):
                x = i * x_spacing
                y = (-(num_per_col[i] - 1) * v_spacing[i]/2) + j * v_spacing[i] # bottom mmi y = 0
                mmi = mmi["op_0"].repositioned(at=(x,y)).owner
                insts += mmi, f"{i},{j}"



        mmi_tree = cast(Mapping[str, fp.ICellRef], insts)
        for i in range(order):
            for j in range(num_per_col[i]):
                if i < order-1:
                    link1 = fp.LinkBetween(start=mmi_tree[f"{i},{j}"]["op_1"],
                                           end=mmi_tree[f"{i+1},{2*j}"]["op_0"],
                                           bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR)
                    insts += link1
                    link2 = fp.LinkBetween(start=mmi_tree[f"{i},{j}"]["op_2"],
                                           end=mmi_tree[f"{i+1},{2*j+1}"]["op_0"],
                                           bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR)
                    insts += link2

        ports += mmi_tree["0,0"]["op_0"].with_name("op_0")
        for i in range(num_per_col[-1]):
            # put ports on the last column of the tree
            ports += mmi_tree[f"{order - 1},{i}"]["op_1"].with_name(f"op_{2*i+1}")
            ports += mmi_tree[f"{order - 1},{i}"]["op_2"].with_name(f"op_{2*i+2}")

        # print(v_spacing)
        # print(mmi_tree["4,1"]["op_0"].position[0])

        heater_wl = 1000
        heater_tl = 400
        heater = pdk.TiNHeaterwithep(waveguide_length=heater_wl, tin_length=heater_tl, tin_box_size=20, contact_box_size=20)

        for i in range (num_per_col[-1]):
            for j in range(2):
                ht_x = mmi_tree[f"{order - 1},{i}"][f"op_{j+1}"].position[0]
                ht_y = mmi_tree[f"{order - 1},{i}"][f"op_{j+1}"].position[1]
                if j == 0:
                    heater = heater["op_0"].repositioned(at=(ht_x + x_spacing / 4, ht_y - end_y_spacing / 4)).owner
                else:
                    heater = heater["op_0"].repositioned(at=(ht_x + x_spacing / 4, ht_y + end_y_spacing / 4)).owner
                # insts += heater, f"ht_{i},{j + 1}"
                insts += heater, f"ht_{2*i+j},{0}"




        mmi_tree = cast(Mapping[str, fp.ICellRef], insts)



        for i in range(num_per_col[-1]):
            for j in range(2):
                link3 = fp.LinkBetween(
                    start=mmi_tree[f"ht_{2*i+j},0"]["op_0"],
                    end=mmi_tree[f"{order - 1},{i}"][f"op_{j+1}"],
                    bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR
                )
                insts += link3




        GC = pdk.GratingCoupler()

        # GC_0 = GC.h_mirrored().translated(mmi_tree[f"ht_{2 ** (order) - 1},0"]["ep_0"].position[0]-100*2**(order-1)-50, 0)
        GC_0 = GC.translated(150, 0).h_mirrored()
        insts += GC_0
        link4 = fp.LinkBetween(start=GC_0["op_0"], end=mmi_tree["0,0"]["op_0"], bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR)
        insts += link4

        for i in range (num_per_col[-1]):
            for j in range(2):
                gc_x = mmi_tree[f"ht_{2*i+j},0"]["op_1"].position[0]
                gc_y = mmi_tree[f"ht_{2*i+j},0"]["op_1"].position[1]
                GC = GC["op_0"].repositioned(at=(gc_x+150, gc_y)).owner
                insts += GC, f"gc_{i},{j+1}"


        mmi_tree = cast(Mapping[str, fp.ICellRef], insts)
        #
        for i in range(num_per_col[-1]):
            for j in range(2):
                link5 = fp.LinkBetween(
                    start=mmi_tree[f"ht_{2*i+j},0"]["op_1"],
                    end=mmi_tree[f"gc_{i},{j+1}"]["op_0"],
                    bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR
                )
                insts += link5

        mmi_tree = cast(Mapping[str, fp.ICellRef], insts)

        BP = pdk.BondPad(pad_width=75, pad_height=75)
        pads_x = numpy.linspace(- heater_wl * 0.1, heater_wl * 0.1 * 2 **(order), 2 **(order))
        pads_left_x = numpy.linspace(100*(2 **(order-1)), 50,  2 **(order-1))
        pads_right_x = numpy.linspace(50, 100*(2 **(order-1)), 2 **(order-1))

        for i in range (2**(order-1)):
            bp_x = pads_left_x[i]
            bp_y = end_y_spacing * (2** (order-1)) / 2
            ht_left_x = mmi_tree[f"ht_{2 ** (order) - 1},0"]["ep_0"].position[0]
            BP_top = BP["ep_0"].repositioned(at=(ht_left_x-bp_x, bp_y+200)).owner
            BP_bot = BP["ep_0"].repositioned(at=(ht_left_x-bp_x, -bp_y-200)).owner
            insts += BP_top, f"BP_{i},0"
            insts += BP_bot, f"BP_{i},1"
        for i in range (2**(order-1)):
            bp_x = pads_right_x[i]
            bp_y = end_y_spacing * (2 ** (order - 1)) / 2
            ht_right_x = mmi_tree[f"ht_{2**(order)-1},0"]["ep_1"].position[0]
            BP_top = BP["ep_0"].repositioned(at=(bp_x+ht_right_x, bp_y + 200)).owner
            BP_bot = BP["ep_0"].repositioned(at=(bp_x+ht_right_x, -bp_y - 200)).owner
            insts += BP_top, f"BP_{i+2**(order-1)},0"
            insts += BP_bot, f"BP_{i+2**(order-1)},1"

        mmi_tree = cast(Mapping[str, fp.ICellRef], insts)

        # top pad

        for i in range(2**(order)):
             if i < 2**(order-1) : # top left part 0-3
                link6 = fp.LinkBetween(
                        start=mmi_tree[f"BP_{i},0"]["ep_0"].with_orientation(degrees=-90),
                        end=mmi_tree[f"ht_{2**(order-1) + i},0"]["ep_0"].with_orientation(degrees=180),
                        metal_line_type=TECH.METAL.M2.W10,
                        min_distance=50,
                        waypoints=[
                            fp.Waypoint(mmi_tree[f"BP_{i},0"]["ep_0"].position[0],mmi_tree[f"BP_{i},0"]["ep_0"].position[1]-37.5-15*(2**(order-1)-i), -90),

                            fp.Waypoint(mmi_tree[f"ht_{2 ** (order) - 1},0"]["ep_0"].position[0]-15*(2**(order-1)-i),end_y_spacing * (2** (order-1)) / 2, -90)
                        ]

                    )
                insts += link6
             else:
                 link7 = fp.LinkBetween(
                     start=mmi_tree[f"BP_{i},0"]["ep_0"].with_orientation(degrees=-90),
                     end=mmi_tree[f"ht_{2**(order-1)+2**order-(i+1)},0"]["ep_1"].with_orientation(degrees=0),
                     metal_line_type=TECH.METAL.M2.W10,
                     min_distance=50,
                     waypoints=[
                         fp.Waypoint(mmi_tree[f"BP_{i},0"]["ep_0"].position[0],
                                     mmi_tree[f"BP_{i},0"]["ep_0"].position[1] - 37.5 - 15 * (i - (2 ** (order - 1)-1)),
                                     -90),
                         #
                         fp.Waypoint(
                             mmi_tree[f"ht_{2 ** (order) - 1},0"]["ep_1"].position[0] + 15 * (i-2 ** (order - 1)+1),
                             end_y_spacing * (2 ** (order - 1)) / 2, -90)
                     ]

                 )
                 insts += link7

        for i in range(2**(order)):
             if i < 2**(order-1) : # bottom left part 0-3
                link8 = fp.LinkBetween(
                        start=mmi_tree[f"BP_{2**(order-1)-1-i},1"]["ep_0"].with_orientation(degrees=90),
                        end=mmi_tree[f"ht_{i},0"]["ep_0"].with_orientation(degrees=180),
                        metal_line_type=TECH.METAL.M2.W10,
                        min_distance=50,
                        waypoints=[
                            fp.Waypoint(mmi_tree[f"BP_{2**(order-1)-1-i},1"]["ep_0"].position[0],
                                    mmi_tree[f"BP_{2**(order-1)-1-i},1"]["ep_0"].position[1] + 37.5 + 15 * (i+1),
                                    90),

                            fp.Waypoint(
                                mmi_tree[f"ht_{2 ** (order) - 1},0"]["ep_0"].position[0] - 15 * (i+1),
                                -(end_y_spacing * (2 ** (order - 1)) / 2), 90)
                        ]


                    )
                insts += link8
             else:
                 link9 = fp.LinkBetween(
                     start=mmi_tree[f"BP_{i},1"]["ep_0"].with_orientation(degrees=90),
                     end=mmi_tree[f"ht_{i-2**(order-1)},0"]["ep_1"].with_orientation(degrees=0),
                     metal_line_type=TECH.METAL.M2.W10,
                     min_distance=50,
                     waypoints=[
                         fp.Waypoint(mmi_tree[f"BP_{i},1"]["ep_0"].position[0],
                                     mmi_tree[f"BP_{i},1"]["ep_0"].position[1] + 37.5 + 15 * (i-(2**(order-1)-1)),
                                     90),

                         fp.Waypoint(
                             mmi_tree[f"ht_{i-2**(order-1)},0"]["ep_1"].position[0] + 15 * (i-(2**(order-1)-1)),
                             -(end_y_spacing * (2 ** (order - 1)) / 2), 90)
                     ]
                 )
                 insts += link9

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += MMITree()
    # device = MMITree()
    # cor = device.polygon_set(layer=TECH.LAYER.FWG_COR)
    # cld = device.polygon_set(layer=TECH.LAYER.FWG_CLD)
    # tre = fp.el.PolygonSet.boolean_sub(cld, cor, layer=TECH.LAYER.FWG_TRE)
    # library += fp.Device(content=[tre.translated(300, 0)], ports=[])

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
    print(library)
