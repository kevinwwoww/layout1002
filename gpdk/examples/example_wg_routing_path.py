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
        gc1 = GC.h_mirrored().translated(100, -100).rotated(degrees=90)
        insts += gc1
        # gc2 = GC.h_mirrored().translated(-100, 0)
        # insts += gc2
        # gc3 = GC.h_mirrored().translated(-100, 100)
        # insts += gc3
        gc4 = GC.h_mirrored().translated(100, 100).rotated(degrees=90)
        insts += gc4
        # gc5 = GC.translated(100, 50)
        # insts += gc5
        # gc6 = GC.translated(100, 150)
        # insts += gc6

        device = fp.LinkBetween(
            start=gc1["op_0"],
            end=gc4["op_0"],
            link_type=TECH.WG.SWG.C.EXPANDED,
            bend_factory=TECH.WG.SWG.C.WIRE.BEND_CIRCULAR,
            # set target_length
            target_length=500
        )

        insts += device

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
    fp.plot(library)