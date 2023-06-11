from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology, PCell

@dataclass(eq=False)
class Linked(PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off
        # call devices
        GC = pdk.GratingCoupler(waveguide_type=TECH.WG.FWG.C.WIRE)
        # Place the devices in different locations and add them to insts
        gc1 = GC.h_mirrored().translated(-100, -100)
        insts += gc1
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
        # Interconnecting device ports by calling the Linked method
        # device = fp.Linked(
        #     Define the type of straight waveguide in automatic routing
            # link_type=TECH.WG.FWG.C.EXPANDED,
            # Define the type of bend in automatic routing
            # bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
            #
            # Define the connection between device ports in links
            # links=[
                # Use >> to define connections between two ports
                # gc1["op_0"] >> fp.Waypoint(-50, -50, 0) >> gc4["op_0"],
                # Use fp.Waypoint(x,y) to define the path point
                # gc2["op_0"] >> fp.Waypoint(0, 50, 0) >> gc5["op_0"],
                # Use LinkBetween to define a separate segment of the connection, and you can modify the type of the straight waveguide and bend with parameters
                # fp.LinkBetween(
                #     start=gc3["op_0"],
                #     end=gc6["op_0"],
                #     link_type=TECH.WG.SWG.C.EXPANDED,
                #     bend_factory=TECH.WG.SWG.C.WIRE.BEND_CIRCULAR,
                #     waypoints=[fp.Waypoint(50, 150, 0)]
                # )
            # ],
            # ports=[],
        # )


        # Add the devices returned by Linked to insts
        # insts += device

        # Interconnecting device ports by calling the create_links method
        device2 = fp.create_links(
            # Define the type of straight waveguide in automatic routing
            link_type=TECH.WG.FWG.C.EXPANDED,
            # Define the type of bend in automatic routing
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
            # Define the connection between device ports in specs
            specs=[
                # Use >> to define connections between two ports
                gc1["op_0"] >> fp.Waypoint(-50, -50, 0) >> gc4["op_0"],
                # Use fp.Waypoint(x,y) to define the path point
                gc2["op_0"] >> fp.Waypoint(0, 50, 0) >> gc5["op_0"],
                # Use LinkBetween to define a separate segment of the connection, and you can modify the type of the straight waveguide and bend with parameters
                fp.LinkBetween(
                    start=gc3["op_0"],
                    end=gc6["op_0"],
                    link_type=TECH.WG.SWG.C.EXPANDED,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_CIRCULAR,
                    waypoints=[fp.Waypoint(50, 150, 0)]
                )
            ],
        )
        # Get and print the length of the three connected links
        length_1 = device2[0].curve_length
        length_2 = device2[1].curve_length
        length_3 = device2[2].curve_length
        print(f"{length_1} \n {length_2} \n {length_3}")
        # Add the device returned by create_links to insts
        insts += device2

        # fmt: on
        return insts, elems, ports

if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    library = fp.Library()

    TECH = get_technology()
    # ================================================
    # fmt: off

    library += Linked()

    # fmt: on
    # ================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)