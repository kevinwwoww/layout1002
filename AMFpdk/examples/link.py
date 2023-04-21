from dataclasses import dataclass
from fnpcell import all as fp
from AMFpdk import all as pdk
from AMFpdk.technology import get_technology


@dataclass(eq=False)
class Link(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        GC = pdk.GratingCoupler(waveguide_type=TECH.WG.CHANNEL.C.WIRE)

        gc1 = GC.h_mirrored().translated(-100, 100)
        gc2 = GC.h_mirrored().translated(-100, 0)
        gc3 = GC.h_mirrored().rotated(degrees=-180).translated(-150, -200)
        gc4 = GC.translated(100, 150)
        gc5 = GC.translated(100, 50)
        gc6 = GC.translated(100, -100)


        #


        device = fp.Linked(
            link_type=TECH.WG.CHANNEL.C.WIRE,
            bend_factory=TECH.WG.CHANNEL.C.WIRE.BEND_CIRCULAR,

            links=[
                gc1["op_0"] >> gc4["op_0"],

                gc2["op_0"] >> fp.Waypoint(0, 50, 0) >> gc5["op_0"],
                #
                fp.LinkBetween(
                    start=gc3["op_0"],
                    end=gc6["op_0"],
                    link_type=TECH.WG.CHANNEL.C.WIRE,
                    bend_factory=TECH.WG.CHANNEL.C.WIRE.BEND_CIRCULAR,
                    waypoints=[fp.Waypoint(50, -50, 0)],
                ),


            ],

            ports=[]
        )

        insts +=  device

        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += Link()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)