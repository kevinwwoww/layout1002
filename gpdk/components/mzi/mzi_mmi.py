import math
from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk.components.mmi.mmi import Mmi
from gpdk.components.straight.straight import Straight
from gpdk.components.bend.bend_euler import BendEuler
from gpdk.technology import get_technology, WG
from gpdk import all as pdk

@dataclass(eq=False)
class MZI_mmi(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        left_mmi = Mmi(n_inputs=1, n_outputs=2)
        right_mmi = Mmi(n_inputs=2, n_outputs=1).translated(100, 20)
        left_mmi_x = left_mmi["op_2"].position[0]
        right_mmi_x = right_mmi["op_0"].position[0]
        # straight_x_top = Straight(length=10).translated((left_mmi_x+right_mmi_x)/2-5, 50)
        # straight_x_bottom = Straight(length=10).translated((left_mmi_x+right_mmi_x)/2-5, -50)

        insts += left_mmi, right_mmi

        # bend_factory = BendEuler(radius_eff=10, waveguide_type=TECH.WG.FWG.C.EXPANDED)

        mzi_up_arm = fp.create_links(
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.EXPANDED.BEND_CIRCULAR,
            specs=[
                # left_mmi["op_2"] >> right_mmi["op_0"],
                fp.LinkBetween(
                    start=left_mmi["op_2"],
                    end = right_mmi["op_0"],
                    target_length=100,
                ),
                fp.LinkBetween(
                    start=left_mmi["op_1"],
                    end= right_mmi["op_1"],
                ),
            ],
        )

        insts += mzi_up_arm

        return insts, elems, ports

if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")

    library = fp.Library()
    TECH = get_technology()

    library += MZI_mmi()

    # fp.export_gds(library, file=gds_file)
    fp.plot(library)
