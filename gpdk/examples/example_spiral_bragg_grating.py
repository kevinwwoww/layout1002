import math
from dataclasses import dataclass
from typing import Any, List, cast, Mapping
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology

@dataclass(eq=False)
class spiral(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        start_period = 0.4046 #um
        end_period = 0.3806 #um
        SiN_length = 120000 #um 12cm = 120000um

        number_of_rec = round(2 * SiN_length / (start_period + end_period)) - 1

        straight = pdk.Straight(length=SiN_length, waveguide_type=TECH.WG.FWG.C.WIRE.updated(core_design_width=2.8))

        center_rec = (1 + number_of_rec) / 2 # where the center of the rectangle is



        for i in range(int(number_of_rec)):
            # x position of each rectangle
            rec_x_position = start_period * (i) - ((start_period - end_period) / number_of_rec) * ((1 + (i - 1) ) * (i - 1) / 2) # um
            # the x position of the center rectangle
            center_rec_x_position = start_period * center_rec - ((start_period - end_period) / number_of_rec) * ((1 + center_rec) * center_rec / 2) # um
            # x position difference compare to the center rectangle, the modulated width from the Gaussian equation will be 0.015um at the center rectangle
            x_position_diff = center_rec_x_position - rec_x_position # um
            # calculate the modulated width base on the equation, here the unit was changed to nm instead of um (need to be confirmed)
            height = 0.3 * math.e ** (-64 * ((x_position_diff * 1e-5 / 0.12 ) ** 4))
            rec = fp.el.Rect(width=0.2,
                             height=2.8 + height,
                             center=(start_period * (i) - ((start_period - end_period) / number_of_rec) * ((1 + (i - 1) ) * (i - 1) / 2) + 0.1, 0),
                             layer=TECH.LAYER.FWG_COR)

            insts += rec
            
    
        insts += straight
        

        


        return insts, elems, ports



if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += spiral()

    # fmt: on
    # ==============================================================

    fp.export_gds(library, file=gds_file)
    # fp.plot(library)