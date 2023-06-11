from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class Circuit05_mzm(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        # fmt: off
        TECH = get_technology()

        ySplitter = pdk.YSplitter(waveguide_type=TECH.WG.SWG.C.WIRE, taper_length=40, bend_radius=50)
        gc = pdk.GratingCoupler(waveguide_type=TECH.WG.SWG.C.WIRE, length=30, half_degrees=20)
        yCombiner = pdk.YCombiner(waveguide_type=TECH.WG.SWG.C.WIRE, taper_length=40, bend_radius=50)

        ySplitter_1 = ySplitter.translated(-150, 0)
        yCombiner_1 = yCombiner.translated(150, 0)
        gc_1 = gc.rotated(degrees=180).translated(-250, 0)
        gc_2 = gc.translated(250, 0)

        device = fp.Linked(
            link_type=TECH.WG.SWG.C.WIRE,
            bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
            links=[
                ySplitter_1["op_0"] >> gc_1["op_0"],
                (ySplitter_1["op_1"] >> yCombiner_1["op_1"], 300),
                (ySplitter_1["op_2"] >> yCombiner_1["op_0"], 400),
                yCombiner_1["op_2"] >> gc_2["op_0"],
            ],
            ports=[]
        )

        insts += device

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off
    from gpdk.components import all as components

    library += Circuit05_mzm()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.export_spc(library, file=gds_file.with_suffix(".spc"), components=components)
    fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=components)
    #  fp.plot(library)
