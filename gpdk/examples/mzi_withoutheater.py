from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk.components.straight.straight import Straight
from gpdk.components.directional_coupler.directional_coupler_bend import DirectionalCouplerBend
from gpdk.technology import get_technology
from gpdk import all as pdk
from gpdk.technology.waveguide_factory import EulerBendFactory, CircularBendFactory

@dataclass(eq=False)
class MZI(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        dc_left = pdk.DirectionalCouplerBend(coupler_spacing=0.7, coupler_length=10, bend_radius=15,
                                              straight_after_bend=10)
        dc_right = pdk.DirectionalCouplerBend(coupler_spacing=0.7, coupler_length=10, bend_radius=15,
                                               straight_after_bend=10).translated(200, 0)



        bend = EulerBendFactory(radius_min=10, l_max=10, waveguide_type=TECH.WG.SWG.C.WIRE)

        mzi = fp.Linked(
            link_type=TECH.WG.SWG.C.WIRE,
            bend_factory=bend,
            links=[
                dc_left["op_2"] >> dc_right["op_1"],
                dc_left["op_3"] >> dc_right["op_0"],
            ],
            ports=[
                dc_left["op_0"].with_name("op_0"),
                dc_left["op_1"].with_name("op_1"),
                dc_right["op_2"].with_name("op_2"),
                dc_right["op_3"].with_name("op_3"),
            ],
        )



        #

        insts += mzi

        # insts += mzi_top
        return insts, elems, ports


if __name__ == "__main__":
    from pathlib import Path
    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    library = fp.Library()
    TECH = get_technology()

    library += MZI()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)