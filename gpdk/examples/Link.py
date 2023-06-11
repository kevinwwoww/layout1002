from  dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology

@dataclass(eq=False)
class Link(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        GC1 = pdk.GratingCoupler(waveguide_type=TECH.WG.FWG.C.WIRE)
        GC2 = pdk.GratingCoupler(waveguide_type=TECH.WG.FWG.C.WIRE)

        # gc1 = GC.h_mirrored().translated(-100, 100)
        # gc2 = GC.h_mirrored().translated(-100, 0)
        gc3 = GC1.h_mirrored().rotated(degrees=-180).translated(-150, 200)
        # gc4 = GC.translated(100, 150)
        # gc5 = GC.translated(100, 50)
        gc6 = GC2.translated(0, 100)
        # gc7 = GC.h_mirrored().translated(-100, -200)
        # gc8 = GC.translated(100, -150)

        # gc9 = GC.h_mirrored().translated(-100, -300)
        # gc10 = GC.translated(100, -250)

        # test = gc9["op_0"] >> gc10["op_0"]
        # insts += test

        link = fp.LinkBetween(
                    start=gc6["op_0"],
                    end=gc3["op_0"],
                    # link_type=TECH.WG.MWG.C.WIRE,
                    bend_factory=TECH.WG.MWG.C.WIRE.BEND_EULER,
                    waypoints=[fp.Offset.from_start(-50, -50)],
                    linking_policy=TECH.LINKING_POLICY.MAX_SWG
                )

        # device = fp.Linked(
        #     link_type=TECH.WG.SWG.C.WIRE,
        #     bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER,
        #
        #     links=[
        #         # gc1["op_0"] >> gc4["op_0"],
        #         #
        #         # gc2["op_0"] >> fp.Waypoint(0, 50, 0) >> gc5["op_0"],
        #         #
        #         fp.LinkBetween(
        #             start=gc3["op_0"],
        #             end=gc6["op_0"],
        #             link_type=TECH.WG.FWG.C.WIRE,
        #             bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER,
        #             # waypoints=[fp.Waypoint(50, -50, 0)],
        #         ),
        #
        #         # TECH.LINKER.SWG_WIRE_FWG_EULER(
        #         #     start=gc7["op_0"],
        #         #     end=gc8["op_0"],
        #         #     waypoints=[fp.Waypoint(50, -150, 0)],
        #         # )
        #
        #     ],
        #
        #     ports=[]
        # )


        insts += gc6, gc3, link



        return insts, elems, ports

if __name__ =="__main__":
    from gpdk.util.path import local_output_file
    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += Link()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
