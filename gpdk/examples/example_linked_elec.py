from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class LinkedElec(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        rm1 = pdk.RingFilter(waveguide_type=TECH.WG.FWG.C.WIRE)
        rm2 = pdk.RingFilter(waveguide_type=TECH.WG.FWG.C.WIRE)

        rm1 = rm1.translated(-200, 100)
        rm2 = rm2.translated(200, 100)

        MT_2 = TECH.METAL.MT.W10.updated(line_width=2)
        MT_4 = TECH.METAL.MT.W10.updated(line_width=4)
        M2_4 = TECH.METAL.M2.W10.updated(line_width=4)
        to = fp.Waypoint
        device = fp.Linked(
            metal_line_type=MT_2,
            metal_min_distance=20,
            links=[
                rm1["op_3"] >> to(0, 150, -90) >> rm2["op_0"],
                rm1["ep_1"].with_orientation(degrees=-90) >> to(0, -10, -90) >> rm2["ep_0"].with_orientation(degrees=-90),
                fp.LinkBetween(
                    rm1["ep_0"].with_orientation(degrees=-90),
                    rm2["ep_1"].with_orientation(degrees=-90),
                    start_distance=40,
                    waylines=[fp.until_y(50), fp.until_x(-20), fp.until_y(-30)],
                    metal_line_type=[(0, MT_4), (10, M2_4), (-30, MT_4)],
                ),
            ],
            ports=[],  # [sb10["op_0"], s40["op_1"]],
        )

        insts += device

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += LinkedElec()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
