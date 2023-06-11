from dataclasses import dataclass
from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk import all as pdk


@dataclass(eq=False)
class Circuit02_ring_loaded_mzi(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        # fmt: off
        TECH = get_technology()
        gc = pdk.GratingCoupler(waveguide_type=TECH.WG.SWG.C.WIRE)
        dc = pdk.DirectionalCouplerSBend(waveguide_type=TECH.WG.SWG.C.WIRE, coupler_spacing=2, bend_degrees=60)
        t = pdk.Fixed_Terminator_TE_1550(length=40, waveguide_type=TECH.WG.SWG.C.WIRE)
        rs = pdk.RingResonatorSingleBus(ring_radius=25, ring_type=TECH.WG.SWG.C.WIRE, bottom_type=TECH.WG.SWG.C.WIRE)
        dc_y = fp.distance_between(dc["op_0"].position, dc["op_3"].position)
        rs_y = fp.distance_between(rs["op_0"].position, rs["op_1"].position)

        gc_0 = gc.rotated(degrees=180).translated(-200, 0)
        gc_1 = gc.rotated(degrees=180).translated(400, 400)
        gc_2 = gc.rotated(degrees=180).translated(400, -400)
        dc_0 = fp.place(dc, "op_0", at=(0, 0))
        dc_1 = fp.place(dc, "op_0", at=(400, 0))
        t_0 = t.rotated(degrees=270).translated(-100, -200)
        rs_0 = rs.translated(dc_y+200-rs_y/2, 200)
        rs_1 = rs.translated(dc_y+200-rs_y/2, -200)

        device = fp.Linked(
            link_type=TECH.WG.SWG.C.WIRE,
            bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
            links=[
                gc_0["op_0"] >> dc_0["op_0"],
                t_0["op_0"] >> dc_0["op_1"],
                rs_0["op_0"] >> dc_0["op_3"],
                rs_1["op_0"] >> dc_0["op_2"],
                rs_0["op_1"] >> dc_1["op_0"],
                rs_1["op_1"] >> dc_1["op_1"],
                gc_1["op_0"] >> dc_1["op_3"],
                gc_2["op_0"] >> dc_1["op_2"],
            ],
            ports=[
            ],
        )
        insts += device

        # fmt: off
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off
    from gpdk.components import all as components

    library += Circuit02_ring_loaded_mzi()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.export_spc(library, file=gds_file.with_suffix(".spc"), components=components)
    fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=components)
    #  fp.plot(library)
