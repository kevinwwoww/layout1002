from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class CreateLinks(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        GC = pdk.GratingCoupler(waveguide_type=TECH.WG.FWG.C.WIRE)       # create gc instance
        gc1 = GC.h_mirrored().translated(-100, -100)                     # place to different places
        insts += gc1                                                     # add to the circuit
        gc2 = GC.h_mirrored().translated(-100, 0)
        insts += gc2
        gc3 = GC.h_mirrored().translated(-100, 100)
        insts += gc3
        gc4 = GC.translated(100, -50)
        insts += gc4
        gc5 = GC.translated(100, 50)
        insts += gc5
        gc6 = GC.translated(100, 150)
        insts += gc6

        links = fp.create_links(                                         # call this function
            link_type=TECH.WG.FWG.C.EXPANDED,                            # the preferred waveguide type of straight link by default
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,               # what bend will be used in the created links by default
            specs=[
                gc1["op_0"]  >> gc4["op_0"],  # simplified usage, gc["op_0"] go through (-50, -50) with direction to the right(angle=0 degrees) and link to gc4["op_0]
                gc2["op_0"] >> fp.Waypoint(0, 50, 0) >> gc5["op_0"],     # `>>` means 'go through/link to'
                fp.LinkBetween(                                          # more customized usage
                    start=gc3["op_0"],
                    end=gc6["op_0"],
                    link_type=TECH.WG.SWG.C.EXPANDED,                    # the preferred waveguide type of straight link for only this link, override the default value
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_CIRCULAR,       # what bend will be used in the created links for only this link, override the default value
                    waypoints=[fp.Waypoint(50, 150, 0)]                  # waypoints for this link
                )
            ],
        )

        # Here we can get the length of the first link created by `fp.create_links`
        length = links[0].curve_length


        insts += links                                                   # add the links created by `fp.create_links` to the circuit

        return insts, elems, ports


    if __name__ == "__main__":
        from pathlib import Path

        gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
        library = fp.Library()

        TECH = get_technology()
        # =============================================================

        # library += Linked()

        # =============================================================
        fp.export_gds(library, file=gds_file)
        fp.plot(library)