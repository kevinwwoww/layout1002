from dataclasses import dataclass
from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk import all as pdk


@dataclass(eq=False)
class Circuit04(fp.PCell):
    dist: float = 1000

    def build(self):
        insts, elems, ports = super().build()
        # fmt: off
        TECH = get_technology()
        dist = self.dist
        gc = pdk.GratingCoupler(waveguide_type=TECH.WG.SWG.C.WIRE)
        dc = pdk.DirectionalCouplerBend(waveguide_type=TECH.WG.SWG.C.WIRE, coupler_spacing=2)

        gc_0 = gc.rotated(degrees=180)
        gc_1 = gc.translated(dist, 0)
        gc_2 = gc.rotated(degrees=180).translated(0, dist)
        gc_3 = gc.translated(dist, dist)
        dc_0 = dc.rotated(degrees=90).translated(dist/2, dist/2)

        device = fp.Linked(
            link_type=TECH.WG.SWG.C.WIRE,
            bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
            links=[
                dc_0["op_3"] >> gc_2["op_0"],
                dc_0["op_0"] >> gc_0["op_0"],
                dc_0["op_1"] >> gc_1["op_0"],
                dc_0["op_2"] >> gc_3["op_0"]
            ],
            ports=[
            ],
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
    from gpdk.components import all as components

    library += Circuit04()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.export_spc(library, file=gds_file.with_suffix(".spc"), components=components)
    fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=components)
    #  fp.plot(library)
