from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class LinkedSplitter(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        # fmt: off
        TECH = get_technology()

        Y1 = pdk.YSplitter(waveguide_type=TECH.WG.MWG.C.EXPANDED, taper_length=40, bend_radius=50)
        Y2 = pdk.YSplitter(waveguide_type=TECH.WG.MWG.C.EXPANDED, taper_length=40, bend_radius=50, transform=fp.rotate(degrees=180))

        YSplitter1 = Y1.translated(-150, 0)
        YSplitter2 = Y2.translated(150, 0)

        # #  fp.plot(fp.Library(sb10,s10,s15,s20,s30,s40))

        device = fp.Linked(
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.MWG.C.EXPANDED.BEND_EULER,
            links=[
                YSplitter1["op_1"] >> YSplitter2["op_2"],
                YSplitter1["op_2"] >> YSplitter2["op_1"],
            ],
            ports=[],
        )

        insts += device

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += LinkedSplitter()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
