import math
from dataclasses import dataclass
from typing import Any, List, cast, Mapping

import numpy as np
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.components.bend.bend_circular import BendCircular90

@dataclass(eq=False)
class spiral_circle(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        total_bends = (1350 - 800) / 30
        # print(total_bends)

        bend_1 = BendCircular90(radius=1350, waveguide_type=TECH.WG.FWG.C.WIRE.updated(core_design_width=2.8))

        for i in range(1):
            # bend_1 = BendCircular90(radius=1350 - i * 30)
            bend_2 = BendCircular90(radius=1350 - i * 30, waveguide_type=TECH.WG.FWG.C.WIRE.updated(core_design_width=2.8)).h_mirrored()
            bend_3 = BendCircular90(radius=1350 - i * 30, waveguide_type=TECH.WG.FWG.C.WIRE.updated(core_design_width=2.8)).c_mirrored()
            bend_4 = BendCircular90(radius=1320 - i * 30, waveguide_type=TECH.WG.FWG.C.WIRE.updated(core_design_width=2.8)).v_mirrored()
            bend_4 = bend_4["op_1"].repositioned(at=(bend_3["op_1"].position[0], bend_3["op_1"].position[1])).owner
            bend_5 = BendCircular90(radius=1350 - (i+1) * 30, waveguide_type=TECH.WG.FWG.C.WIRE.updated(core_design_width=2.8))

            link = fp.Linked(
                link_type=TECH.WG.FWG.C.WIRE.updated(core_design_width=2.8),
                links=[bend_4["op_0"] >> bend_5["op_0"]],
                ports=[]
            )
            # bend_2_length = bend_2.curve_length
            # bend_3_length = bend_3.curve_length
            # bend_4_length = bend_4.curve_length
            # bend_5_length = bend_5.curve_length
            # add = bend_2_length + bend_3_length + bend_4_length + bend_5_length


            insts += bend_2, f"bend_2_{i}"
            insts += bend_3, f"bend_3_{i}"
            insts += bend_4, f"bend_4_{i}"
            insts += bend_5, f"bend_5_{i}"
            insts += link, f"link_{i}"
        bend = cast(Mapping[str, fp.ICellRef], insts)

        sum = 0
        for i in range(1):
            bend_2_length = bend[f"bend_2_{i}"].curve_length
            bend_3_length = bend[f"bend_3_{i}"].curve_length
            bend_4_length = bend[f"bend_4_{i}"].curve_length
            bend_5_length = bend[f"bend_5_{i}"].curve_length

            sum = sum + bend_2_length + bend_3_length + bend_4_length + bend_5_length

        # print(sum)

        start_period = 0.4046  # um
        end_period = 0.3806  # um
        SiN_length = 120  # um 12cm = 120000um

        number_of_rec = round(2 * SiN_length / (start_period + end_period)) - 1

        center_rec = (1 + number_of_rec) / 2  # where the center of the rectangle is

        for i in range(4000):
            # x position of each rectangle
            rec_x_position = start_period * (i) - ((start_period - end_period) / number_of_rec) * (
                        (1 + (i - 1)) * (i - 1) / 2)
            rec_x_position_next = start_period * (i+1) - ((start_period - end_period) / number_of_rec) * (
                    (1 + (i)) * (i) / 2)
            cycle_length = rec_x_position_next - rec_x_position # um
            # um

            # the x position of the center rectangle
            center_rec_x_position = start_period * center_rec - ((start_period - end_period) / number_of_rec) * (
                        (1 + center_rec) * center_rec / 2)  # um
            # x position difference compare to the center rectangle, the modulated width from the Gaussian equation will be 0.015um at the center rectangle
            x_position_diff = center_rec_x_position - rec_x_position  # um
            # calculate the modulated width base on the equation, here the unit was changed to nm instead of um (need to be confirmed)
            height = 0.3 * math.e ** (-64 * ((x_position_diff * 1e-5 / 0.12) ** 4))
            rec = fp.el.Rect(width=2.8 + height,
                             height=0.2,
                             center=(0, 0),
                             layer=TECH.LAYER.FWG_COR)

            angle = (360 * rec_x_position_next) / 2 / 1350
            # print(angle)
            # print(rec_x_position)
            rec_translate_x_position = 1350 * math.cos(math.pi / (180 / angle))
            rec_translate_y_position = 1350 * math.sin(math.pi / (180 / angle))

            # print(rec_translate_y_position)
            # print(math.cos(math.pi / (180 / angle)))




            rec = rec.translated(rec_translate_x_position, rec_translate_y_position)
            rec = rec.rotated(radians=(math.pi / (180 / angle)), origin=(rec_translate_x_position, rec_translate_y_position))

            insts += rec


        # link = fp.Linked(
        #     link_type=TECH.WG.FWG.C.WIRE,
        #     links=[bend_4["op_0"] >> bend_5["op_0"]],
        #     ports=[]
        #
        # )
        #
        insts += bend_1

        rec_test = fp.el.Rect(width=100, height=30, center=(0, 0), layer=TECH.LAYER.FWG_COR)
        rec_test = rec_test.rotated()
        insts += rec_test

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += spiral_circle()


    # fmt: on
    # ==============================================================

    fp.export_gds(library, file=gds_file)
    # fp.plot(library)

