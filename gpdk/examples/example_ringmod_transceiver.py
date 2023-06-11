from dataclasses import dataclass
from typing import Any, List
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class Transceiver(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        MT_21 = TECH.METAL.MT.W20.updated(line_width=21)
        MT_10 = TECH.METAL.MT.W20.updated(line_width=10)
        M1_10 = TECH.METAL.M1.W20.updated(line_width=10)
        N = 4
        radius = 10
        radius_add = 0.025
        spacing = 450
        gap = 0.31
        gap_monitor = 0.45

        RingModulator: List[Any] = [None] * N
        RingFilter: List[Any] = [None] * N
        for i in range(N):
            RingModulator[i] = pdk.RingModulator(gap_monitor=gap_monitor, gap=gap, ring_radius=radius + radius_add * i, waveguide_type=TECH.WG.FWG.C.WIRE)
            RingFilter[i] = pdk.RingFilter(gap_monitor=gap_monitor, gap=gap, ring_radius=radius + radius_add * i, waveguide_type=TECH.WG.FWG.C.WIRE)
        EdgeCoupler = pdk.Fixed_Edge_Coupler()
        EdgeCoupler_M = pdk.Fixed_Edge_Coupler(transform=fp.rotate(degrees=180))
        Terminator = pdk.Fixed_Terminator_TE_1550(length=10, waveguide_type=TECH.WG.FWG.C.WIRE)
        Terminator_M = pdk.Fixed_Terminator_TE_1550(length=10, waveguide_type=TECH.WG.FWG.C.WIRE, transform=fp.rotate(degrees=180))
        PhotoDdtector = pdk.Fixed_Photo_Detector(transform=fp.rotate(degrees=180))
        PhotoDdtector_H = pdk.Fixed_Photo_Detector(transform=fp.rotate(degrees=-90))
        Ysplitter = pdk.YSplitter(waveguide_type=TECH.WG.FWG.C.WIRE, taper_length=20, bend_radius=10, out_degrees=90, center_waveguide_length=10)
        Straight = pdk.Straight(length=10, waveguide_type=TECH.WG.FWG.C.WIRE)
        BondPad_75 = pdk.BondPad(pad_width=75, pad_height=75)
        BondPad_100 = pdk.BondPad(pad_width=100, pad_height=100)
        M_Taper_1 = pdk.MTaper(initial_width=2, final_width=10, final_offset=-4, length=20)
        M_Taper_2 = pdk.MTaper(initial_width=21, final_width=75, length=20)
        M_Taper_3 = pdk.MTaper(initial_width=10, final_width=75, length=20)
        M_Taper_4 = pdk.MTaper(initial_width=10, final_width=100, length=20)
        M_Taper_5 = pdk.MTaper(initial_width=21, final_width=100, length=20)
        M_Taper_6 = pdk.MTaper(initial_width=20, final_width=75, length=20)

        EC1 = EdgeCoupler.translated(0, 0)
        EC2 = EdgeCoupler_M.translated(7700, 0)
        EC3 = EdgeCoupler_M.translated(7700, 775)

        RM: List[Any] = [None] * N
        RF: List[Any] = [None] * N
        ST: List[Any] = [None] * N
        for i in range(N):
            RM[i] = RingModulator[i].translated(2140 + spacing * i, 600)
            RF[i] = RingFilter[i].translated(7610 - spacing * i, 373)
            ST[i] = Straight.translated(2050 + spacing * i, 680 + 5 * i)

        ST5 = Straight.translated(2050, 0)
        ST6 = Straight.translated(6000, 373)

        PD: List[Any] = [None] * N * 2
        for i in range(N):
            PD[i] = PhotoDdtector.translated(7670 - spacing * i, 617)
            PD[N + i] = PhotoDdtector_H.translated(150 + 100 * i, 650 - 60 * i)

        TM: List[Any] = [None] * N * 2
        for i in range(N):
            TM[i] = Terminator.translated(
                2152.25 + radius + spacing * i + radius_add * i,
                600 + TECH.WG.FWG.C.WIRE.core_width * 2 + radius * 2 + gap + gap_monitor + radius_add * 2 * i,
            )
            TM[N + i] = Terminator_M.translated(
                7597.75 - radius - spacing * i - radius_add * i,
                373 + TECH.WG.FWG.C.WIRE.core_width * 2 + radius * 2 + gap + gap_monitor + radius_add * 2 * i,
            )

        YS = Ysplitter.translated(7400, 170)
        ST7 = Straight.translated(3800, 170)
        ST8 = Straight.translated(7650, 200)

        for i in range(9):
            insts += BondPad_75.translated(100 + i * 100, 797.5)
            if i < 5:
                insts += M_Taper_2.rotated(degrees=90).translated(100 + i * 100, 740)
            else:
                insts += M_Taper_3.rotated(degrees=90).translated(100 * i + 100, 740)

        for i in range(N):
            insts += MT_21(curve=fp.g.Polyline([(200 + i * 100, 740), (200 + i * 100, 589.1 - i * 60), (157.125 + i * 100, 589.1 - i * 60)]))

        insts += [
            MT_21(curve=fp.g.Polyline([(100, 740), (100, 300), (3502.349, 300)])),
            MT_21(curve=fp.g.Polyline([(142.875, 589.1), (90, 589.1)])),
            MT_21(curve=fp.g.Polyline([(242.875, 529.1), (195.63, 529.1), (195.63, 459.1), (90, 459.1)])),
            MT_21(curve=fp.g.Polyline([(342.875, 469.1), (295.63, 469.1), (295.63, 399.1), (90, 399.1)])),
            MT_21(curve=fp.g.Polyline([(442.875, 409.1), (395.63, 409.1), (395.63, 310)])),
        ]
        for i in range(N):
            EL = MT_10(
                curve=fp.g.Polyline(
                    [
                        (600 + i * 100, 740),
                        (600 + i * 100, 370 + i * 60),
                        (3265 - i * spacing, 370 + i * 60),
                        (3482.651 - i * spacing, 574.725),
                        (3482.651 - i * spacing, 594.725),
                    ]
                )
            )
            insts += EL
            insts += M_Taper_1.h_mirrored(x=0).translated(3490 - i * spacing, 610.935)
            insts += M_Taper_1.translated(3490 - i * spacing, 610.935)
            EL1 = MT_10(curve=fp.g.Polyline([(3510 - i * spacing, 606.935), (3640 - i * spacing, 606.935), (3640 - i * spacing, 648.76)]))
            insts += EL1
            EL2 = MT_10(curve=fp.g.Polyline([(3470 - i * spacing, 606.935), (3340.5 - i * spacing, 606.935), (3340 - i * spacing, 648.76)]))
            insts += EL2
            insts += M_Taper_4.rotated(degrees=90).translated(3640 - i * spacing, 648.76)
            insts += M_Taper_4.rotated(degrees=90).translated(3340 - i * spacing, 648.76)
            EL3 = MT_10(
                curve=fp.g.Polyline(
                    [
                        (3490 - i * spacing, 628.76 - i * radius_add * 2),
                        (3490 - i * spacing, 648.76 - i * radius_add * 2),
                    ]
                )
            )
            insts += EL3
            insts += M_Taper_4.rotated(degrees=90).translated(3490 - i * spacing, 648.76)
            for j in range(3):
                insts += BondPad_100.translated(3340 + j * 150 - i * spacing, 718.76)

            EL4 = MT_10(curve=fp.g.Polyline([(3497.349 - i * spacing, 594.725), (3497.349 - i * spacing, 574.725)]))
            insts += EL4
            VIA1 = fp.el.Rect(width=5, height=5, center=(3497.349 - i * spacing, 577.225), layer=TECH.LAYER.VIA1_DRW)
            elems += VIA1
            VIA2 = fp.el.Rect(width=5, height=5, center=(3497.349 - i * spacing, 300), layer=TECH.LAYER.VIA1_DRW)
            elems += VIA2
            EL5 = M1_10(curve=fp.g.Polyline([(3497.349 - i * spacing, 579.725), (3497.349 - i * spacing, 289.5)]))
            insts += EL5
        for i in range(N):
            if i < 1:
                insts += MT_10(curve=fp.g.Polyline([(4640 + i * 100, 630), (4640 + i * 100, 365.225), (6255.151 + i * spacing, 365.225)]))
            else:
                insts += MT_10(
                    curve=fp.g.Polyline(
                        [
                            (4640 + i * 100, 630),
                            (4640 + i * 100, 365.225 + i * 50),
                            (6030 + i * spacing, 365.225 + i * 50),
                            (6030 + i * spacing, 365.225),
                            (6255.151 + i * spacing, 365.225),
                        ],
                    )
                )

            insts += M_Taper_3.rotated(degrees=90).translated(4640 + i * 100, 630)
            insts += BondPad_75.translated(4640 + i * 100, 687.5)
            insts += MT_10(curve=fp.g.Polyline([(6267.349 + i * spacing, 367.725), (6267.349 + i * spacing, 270)]))
            insts += M_Taper_5.rotated(degrees=-90).translated(6260.1 + i * spacing, 609.875)
            insts += MT_21(
                curve=fp.g.Polyline(
                    [
                        (6248.6 + 10.5 - 150 + i * spacing, 624.125),
                        (6248.6 + 10.5 - 150 + i * spacing, 609.875 - 20),
                        (6248.6 + 10.5 + 150 + i * spacing, 609.875 - 20),
                        (6248.6 + 10.5 + 150 + i * spacing, 624.125),
                    ]
                )
            )
            for j in range(3):
                insts += M_Taper_5.rotated(degrees=90).translated(6248.6 - 150 + j * 150 + 10.5 + i * spacing, 624.125)
                insts += BondPad_100.translated(6248.6 - 150 + 10.5 + j * 150 + i * spacing, 694.125)

        insts += BondPad_75.translated(4540, 687.5)
        insts += M_Taper_6.rotated(degrees=90).translated(4540, 630)
        insts += MT_21(curve=fp.g.Polyline([(4540, 630), (4540, 280), (7622.350, 280)]))

        device = fp.Linked(
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER,
            links=[
                RM[0]["op_0"] >> ST[0]["op_1"],
                RM[0]["op_1"] >> ST5["op_1"],
                EC1["op_0"] >> ST5["op_0"],
                RM[0]["op_2"] >> RM[1]["op_1"],
                RM[0]["op_3"] >> TM[0]["op_0"],
                RM[1]["op_0"] >> ST[1]["op_1"],
                RM[1]["op_2"] >> RM[2]["op_1"],
                RM[1]["op_3"] >> TM[1]["op_0"],
                RM[2]["op_0"] >> ST[2]["op_1"],
                RM[2]["op_2"] >> RM[3]["op_1"],
                RM[2]["op_3"] >> TM[2]["op_0"],
                RM[3]["op_0"] >> ST[3]["op_1"],
                RM[3]["op_2"] >> ST7["op_0"],
                YS["op_0"] >> ST7["op_1"],
                RM[3]["op_3"] >> TM[3]["op_0"],
                RF[0]["op_0"] >> TM[4]["op_0"],
                RF[0]["op_1"] >> RF[1]["op_2"],
                RF[0]["op_2"] >> ST8["op_1"],
                YS["op_2"] >> ST8["op_0"],
                RF[0]["op_3"] >> PD[0]["op_0"],
                RF[1]["op_0"] >> TM[5]["op_0"],
                RF[1]["op_1"] >> RF[2]["op_2"],
                RF[1]["op_3"] >> PD[1]["op_0"],
                RF[2]["op_0"] >> TM[6]["op_0"],
                RF[2]["op_1"] >> RF[3]["op_2"],
                RF[2]["op_3"] >> PD[2]["op_0"],
                RF[3]["op_0"] >> TM[7]["op_0"],
                RF[3]["op_1"] >> ST6["op_1"],
                EC3["op_0"] >> ST6["op_0"],
                RF[3]["op_3"] >> PD[3]["op_0"],
                YS["op_1"] >> EC2["op_0"],
                PD[4]["op_0"] >> ST[3]["op_0"],
                PD[5]["op_0"] >> ST[2]["op_0"],
                PD[6]["op_0"] >> ST[1]["op_0"],
                PD[7]["op_0"] >> ST[0]["op_0"],
            ],
            ports=[
                RM[0]["ep_0"].with_name("RM[0]_ep_0"),
                RM[0]["ep_1"].with_name("RM[0]_ep_1"),
                RM[0]["ep_2"].with_name("RM[0]_ep_2"),
                RM[0]["ep_3"].with_name("RM[0]_ep_3"),
                RM[1]["ep_0"].with_name("RM[1]_ep_0"),
                RM[1]["ep_1"].with_name("RM[1]_ep_1"),
                RM[1]["ep_2"].with_name("RM[1]_ep_2"),
                RM[1]["ep_3"].with_name("RM[1]_ep_3"),
                RM[2]["ep_0"].with_name("RM[2]_ep_0"),
                RM[2]["ep_1"].with_name("RM[2]_ep_1"),
                RM[2]["ep_2"].with_name("RM[2]_ep_2"),
                RM[2]["ep_3"].with_name("RM[2]_ep_3"),
                RM[3]["ep_0"].with_name("RM[3]_ep_0"),
                RM[3]["ep_1"].with_name("RM[3]_ep_1"),
                RM[3]["ep_2"].with_name("RM[3]_ep_2"),
                RM[3]["ep_3"].with_name("RM[3]_ep_3"),
                RF[0]["ep_0"].with_name("RF[0]_ep_0"),
                RF[0]["ep_1"].with_name("RF[0]_ep_1"),
                RF[1]["ep_0"].with_name("RF[1]_ep_0"),
                RF[1]["ep_1"].with_name("RF[1]_ep_1"),
                RF[2]["ep_0"].with_name("RF[2]_ep_0"),
                RF[2]["ep_1"].with_name("RF[2]_ep_1"),
                RF[3]["ep_0"].with_name("RF[3]_ep_0"),
                RF[3]["ep_1"].with_name("RF[3]_ep_1"),
                PD[0]["ep_1"].with_name("PD[0]_ep_2"),
                PD[0]["ep_0"].with_name("PD[0]_ep_3"),
                PD[1]["ep_1"].with_name("PD[1]_ep_2"),
                PD[1]["ep_0"].with_name("PD[1]_ep_3"),
                PD[2]["ep_1"].with_name("PD[2]_ep_2"),
                PD[2]["ep_0"].with_name("PD[2]_ep_3"),
                PD[3]["ep_1"].with_name("PD[3]_ep_2"),
                PD[3]["ep_0"].with_name("PD[3]_ep_3"),
                PD[4]["ep_1"].with_name("PD[4]_ep_2"),
                PD[4]["ep_0"].with_name("PD[4]_ep_3"),
                PD[5]["ep_1"].with_name("PD[5]_ep_2"),
                PD[5]["ep_0"].with_name("PD[5]_ep_3"),
                PD[6]["ep_1"].with_name("PD[6]_ep_2"),
                PD[6]["ep_0"].with_name("PD[6]_ep_3"),
                PD[7]["ep_1"].with_name("PD[7]_ep_2"),
                PD[7]["ep_0"].with_name("PD[7]_ep_3"),
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

    library += Transceiver()

    # fmt: on
    # =============================================================
    from gpdk.components import all as components

    fp.export_gds(library, file=gds_file)
    fp.export_spc(library, file=gds_file.with_suffix(".spc"), components=components)
    fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=components)
    # fp.plot(library)
