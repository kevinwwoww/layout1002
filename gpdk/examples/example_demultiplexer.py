from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class Demultiplexer(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        # fmt: off
        TECH = get_technology()

        waveguide_type = TECH.WG.SWG.C.WIRE.updated(core_layout_width=1.5)
        s_w = pdk.Straight(length=50, waveguide_type=waveguide_type)
        ec = pdk.Fixed_Edge_Coupler(name="e")
        dc31 = pdk.DirectionalCouplerBend(
            coupler_spacing=1.5,
            coupler_length=31,
            bend_radius=25,
            waveguide_type=TECH.WG.MWG.C.WIRE,
        )
        dc18 = pdk.DirectionalCouplerBend(
            coupler_spacing=1.5,
            coupler_length=18,
            bend_radius=25,
            waveguide_type=TECH.WG.MWG.C.WIRE,
        )
        dc3 = pdk.DirectionalCouplerBend(
            coupler_spacing=1.5,
            coupler_length=3,
            bend_radius=25,
            waveguide_type=TECH.WG.MWG.C.WIRE,
        )
        tm = pdk.Fixed_Terminator_TE_1550(
            length=30,
            waveguide_type=TECH.WG.MWG.C.WIRE,
            transform=fp.rotate(degrees=180),
        )
        pd = pdk.Fixed_Photo_Detector(name="p")

        ec_0 = ec.translated(-100, 150)
        ec_1 = ec.translated(-100, -150)
        s_w_0 = s_w.translated(50, 150)
        s_w_1 = s_w.translated(50, -150)

        dc_0 = dc31.translated(200, 0)

        dc_1 = dc18.translated(400, 0)
        dc_2 = dc3.translated(600, 0)

        dc_3_0 = dc31.translated(dc_2["op_3"].position[0] - dc31["op_0"].position[0], 180)
        dc_3_1 = dc31.translated(dc_2["op_2"].position[0] - dc31["op_1"].position[0], -180)

        t_0 = tm.translated(500, 280)
        t_1 = tm.translated(500, -280)

        dc_4_0 = dc3.translated(820, 180)
        dc_4_1 = dc3.translated(820, -180)

        pd_0 = pd.translated(970, 300)
        pd_1 = pd.translated(970, 100)
        pd_2 = pd.translated(970, -100)
        pd_3 = pd.translated(970, -300)

        to = fp.Waypoint
        device = fp.Linked(
            link_type=TECH.WG.SWG.C.WIRE,
            links=[
                ec_0["op_0"] >> s_w_0["op_0"],
                s_w_0["op_1"] >> dc_0["op_0"],
                ec_1["op_0"] >> s_w_1["op_0"],
                s_w_1["op_1"] >> dc_0["op_1"],
                #
                dc_0["op_3"] >> to(300, 250, 0) >> dc_1["op_0"],
                dc_0["op_2"] >> to(300, -100, 0) >> dc_1["op_1"],
                #
                dc_1["op_3"] >> to(500, 100, 0) >> dc_2["op_0"],
                dc_1["op_2"] >> to(500, -250, 0) >> dc_2["op_1"],
                #
                dc_2["op_3"] >> dc_3_0["op_1"],
                dc_2["op_2"] >> dc_3_1["op_0"],
                t_0["op_0"] >> dc_3_0["op_0"],
                t_1["op_0"] >> dc_3_1["op_1"],
                dc_3_0["op_3"] >> to(750, 300, 0) >> dc_4_0["op_0"],
                dc_3_0["op_2"] >> to(750, 100, 0) >> dc_4_0["op_1"],
                dc_3_1["op_3"] >> to(750, -100, 0) >> dc_4_1["op_0"],
                dc_3_1["op_2"] >> to(750, -300, 0) >> dc_4_1["op_1"],
                #
                dc_4_0["op_3"] >> to(900, 300, 0) >> pd_0["op_0"],
                dc_4_0["op_2"] >> to(900, 100, 0) >> pd_1["op_0"],
                dc_4_1["op_3"] >> to(900, -100, 0) >> pd_2["op_0"],
                dc_4_1["op_2"] >> to(900, -300, 0) >> pd_3["op_0"],
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

    library += Demultiplexer()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
