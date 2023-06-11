from dataclasses import dataclass

from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class Demultiplexer2(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        # fmt: off
        TECH = get_technology()

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
        pd_1 = pd.translated(970, 60)
        pd_2 = pd.translated(970, -60)
        pd_3 = pd.translated(970, -300)

        links = fp.create_links(
            link_type=TECH.WG.SWG.C.WIRE,
            bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
            specs=[
                ec_0["op_0"] >> dc_0["op_0"],
                ec_1["op_0"] >> dc_0["op_1"],
                #
                (dc_0["op_3"] >> dc_1["op_0"], 500),
                dc_0["op_2"] >> dc_1["op_1"],
                dc_1["op_3"] >> dc_2["op_0"],
                (dc_1["op_2"] >> dc_2["op_1"], 500),
                #
                dc_2["op_3"] >> dc_3_0["op_1"],
                dc_2["op_2"] >> dc_3_1["op_0"],
                t_0["op_0"] >> dc_3_0["op_0"],
                t_1["op_0"] >> dc_3_1["op_1"],
                #
                (dc_3_0["op_3"] >> dc_4_0["op_0"], 300),
                dc_3_0["op_2"] >> dc_4_0["op_1"],
                dc_3_1["op_3"] >> dc_4_1["op_0"],
                (dc_3_1["op_2"] >> dc_4_1["op_1"], 300),
                #
                dc_4_0["op_3"] >> pd_0["op_0"],
                dc_4_0["op_2"] >> pd_1["op_0"],
                dc_4_1["op_3"] >> pd_2["op_0"],
                dc_4_1["op_2"] >> pd_3["op_0"],
            ],
        )

        insts += ec_0, 'ec_0'
        insts += ec_1, 'ec_1'
        insts += dc_0, 'dc_0'
        insts += dc_1, 'dc_1'
        insts += dc_2, 'dc_2'
        insts += dc_3_0, 'dc_3_0'
        insts += dc_3_1, 'dc_3_1'
        insts += t_0, 't_0'
        insts += t_1, 't_1'
        insts += dc_4_0, 'dc_4_0'
        insts += dc_4_1, 'dc_4_1'
        insts += pd_0, 'pd_0'
        insts += pd_1, 'pd_1'
        insts += pd_2, 'pd_2'
        insts += pd_3, 'pd_3'
        insts += links

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.components import all as components
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    naming_table = {}
    # =============================================================
    # fmt: off

    d = Demultiplexer2()
    library += d

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file, cell_naming_table=naming_table)
    fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=components)
    # fp.plot(library)

    pd_2 = d.get("pd_2", pdk.Fixed_Photo_Detector)
    assert pd_2 is not None
    pd_2_op_0 = pd_2["op_0"]
    assert pd_2_op_0.position == (970, -60)

    pd_3 = d.translated(20, 0).get("pd_3")
    assert pd_3 is not None
    pd_3_op_0 = pd_3["op_0"]
    assert pd_3_op_0.position == (990, -300)  # 970+20
