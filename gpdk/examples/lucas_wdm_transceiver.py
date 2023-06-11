from dataclasses import dataclass
from typing import Any, List, cast, Mapping
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class Transceiver(fp.PCell):

    radius: float = fp.PositiveFloatParam(default=10)
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        N = 4
        radius = self.radius
        radius_add = 0.025
        spacing = 450
        gap = 0.31
        gap_monitor = 0.45


        RingModulator = pdk.RingModulator(gap_monitor=gap_monitor, gap=gap, ring_radius=radius + radius_add , waveguide_type=TECH.WG.FWG.C.WIRE)
        RingFilter = pdk.RingFilter(gap_monitor=gap_monitor, gap=gap, ring_radius=radius + radius_add, waveguide_type=TECH.WG.FWG.C.WIRE)
        EdgeCoupler = pdk.Fixed_Edge_Coupler()
        EdgeCoupler_M = pdk.Fixed_Edge_Coupler(transform=fp.rotate(degrees=180))
        Terminator = pdk.Fixed_Terminator_TE_1550(length=10, waveguide_type=TECH.WG.FWG.C.WIRE)
        Terminator_M = pdk.Fixed_Terminator_TE_1550(length=10, waveguide_type=TECH.WG.FWG.C.WIRE, transform=fp.rotate(degrees=180))
        PhotoDdtector = pdk.Fixed_Photo_Detector(transform=fp.rotate(degrees=180))
        PhotoDdtector_H = pdk.Fixed_Photo_Detector(transform=fp.rotate(degrees=-90))
        Ysplitter = pdk.YSplitter(waveguide_type=TECH.WG.FWG.C.WIRE, taper_length=20, bend_radius=10, out_degrees=90, center_waveguide_length=10)
        Straight = pdk.Straight(length=10, waveguide_type=TECH.WG.FWG.C.WIRE)



        # ec1=left, ec2/3=right
        EC1 = EdgeCoupler.translated(0, 0)
        EC2 = EdgeCoupler_M.translated(7700, 0)
        EC3 = EdgeCoupler_M.translated(7700, 775)
        insts += EC1, EC2, EC3

        # RM for transmitter left, RF for receiver right
        for i in range(N):
            RM = RingModulator.translated(2140 + spacing * i, 600)
            insts += RM, f"RM_{i}"
        tranceiver = cast(Mapping[str, fp.ICellRef], insts)
        for i in range(N):
            RF = RingFilter.translated(7610 - spacing * i, 373)
            insts += RF, f"RF_{i}"
        tranceiver = cast(Mapping[str, fp.ICellRef], insts)

        # 0-3 receiver PD, 4-7 transmitter PD
        for i in range(N):
            PD = PhotoDdtector.translated(7670 - spacing * i, 617)
            insts += PD, f"PD_{i}"
        tranceiver = cast(Mapping[str, fp.ICellRef], insts)
        for i in range(N):
            PD = PhotoDdtector_H.translated(150 + 100 * i, 650 - 60 * i)
            insts += PD, f"PD_{N+i}"
        tranceiver = cast(Mapping[str, fp.ICellRef], insts)

        YS = Ysplitter.translated(7400, 170)
        insts += YS

        optical_link1 = fp.create_links(
            link_type=TECH.WG.FWG.C.EXPANDED,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER,
            specs=[
                fp.LinkBetween(
                    start=EC1["op_0"],
                    end=tranceiver["RM_0"]["op_1"],
                    waylines=[fp.until_x(tranceiver["RM_0"]["op_1"].position[0]-70)]
                ),
                tranceiver["RM_0"]["op_2"] >> tranceiver["RM_1"]["op_1"],
                tranceiver["RM_1"]["op_2"] >> tranceiver["RM_2"]["op_1"],
                tranceiver["RM_2"]["op_2"] >> tranceiver["RM_3"]["op_1"],
                fp.LinkBetween(
                    start=tranceiver["RM_3"]["op_2"],
                    end=YS["op_0"],
                    waylines=[fp.until_x(tranceiver["RM_3"]["op_2"].position[0]+300)]
                ),
                YS["op_1"] >> EC2["op_0"],
                fp.LinkBetween(
                    start=YS["op_2"],
                    end=tranceiver["RF_0"]["op_2"],
                    waylines=[fp.until_x(tranceiver["RF_0"]["op_2"].position[0]+70)]
                ),
                tranceiver["RF_0"]["op_1"] >> tranceiver["RF_1"]["op_2"],
                tranceiver["RF_1"]["op_1"] >> tranceiver["RF_2"]["op_2"],
                tranceiver["RF_2"]["op_1"] >> tranceiver["RF_3"]["op_2"],
                fp.LinkBetween(
                    start=tranceiver["RF_0"]["op_3"],
                    end=tranceiver["PD_0"]["op_0"],
                    waylines=[fp.until_x(tranceiver["RF_0"]["op_3"].position[0]+100)]
                ),
                fp.LinkBetween(
                    start=tranceiver["RF_1"]["op_3"],
                    end=tranceiver["PD_1"]["op_0"],
                    waylines=[fp.until_x(tranceiver["RF_1"]["op_3"].position[0] + 100)]
                ),
                fp.LinkBetween(
                    start=tranceiver["RF_2"]["op_3"],
                    end=tranceiver["PD_2"]["op_0"],
                    waylines=[fp.until_x(tranceiver["RF_2"]["op_3"].position[0] + 100)]
                ),
                fp.LinkBetween(
                    start=tranceiver["RF_3"]["op_3"],
                    end=tranceiver["PD_3"]["op_0"],
                    waylines=[fp.until_x(tranceiver["RF_3"]["op_3"].position[0] + 100)]
                ),
                fp.LinkBetween(
                    start=tranceiver["RF_3"]["op_1"],
                    end=EC3["op_0"],
                    waylines=[fp.until_x(tranceiver["RF_3"]["op_1"].position[0]-250)]
                )
            ]
        )
        insts += optical_link1
        for i in range(N):
            optical_link2 = fp.LinkBetween(
                start=tranceiver[f"RM_{i}"]["op_0"],
                end=tranceiver[f"PD_{2*N-1-i}"]["op_0"],
                waypoints=[
                    fp.Waypoint(
                        tranceiver[f"RM_{i}"]["op_0"].position[0]-70,
                        tranceiver[f"RM_{i}"]["op_0"].position[1]+ 50+ 5* i,
                        90
                    )
                ]
            )
            insts += optical_link2


        BondPad_75 = pdk.BondPad(pad_width=75, pad_height=75)
        BondPad_100 = pdk.BondPad(pad_width=100, pad_height=100)
        M_Taper_1 = pdk.MTaper(initial_width=2, final_width=10, final_offset=-4, length=20)
        M_Taper_2 = pdk.MTaper(initial_width=21, final_width=75, length=20)
        M_Taper_3 = pdk.MTaper(initial_width=10, final_width=75, length=20)
        M_Taper_4 = pdk.MTaper(initial_width=10, final_width=100, length=20)
        M_Taper_5 = pdk.MTaper(initial_width=21, final_width=100, length=20)
        M_Taper_6 = pdk.MTaper(initial_width=20, final_width=75, length=20)

        #define tx pad position
        for i in range(9):
            BP_tr = BondPad_75.translated(100 + i * 100, 797.5)
            if i < 5:
                BP1 = M_Taper_2.rotated(degrees=90).translated(100 + i * 100, 740)
                insts += BP1, f"tr_pad_taper_{i}"
            else:
                BP2 = M_Taper_3.rotated(degrees=90).translated(100 + i * 100, 740)
                insts += BP2, f"tr_pad_taper_{i}"
            insts += BP_tr, f"tr_pad_{i}"
        tranceiver = cast(Mapping[str, fp.ICellRef], insts)
        # define ring modulator pad position
        for i in range(N):
            for j in range(3):
                BP_rm = BondPad_100.translated(3340 + j * 150 - i * spacing, 797.5)
                BP_taper = M_Taper_4.rotated(degrees=90).translated(3340 + j * 150 - i * spacing, 727.5)
                insts += BP_rm, f"rm_pad_{i}, {j}"
                insts += BP_taper, f"rm_pad_taper{i}, {j}"
        tranceiver = cast(Mapping[str, fp.ICellRef], insts)
        # define rx pad position
        for i in range(5):
            BP_re = BondPad_75.translated(4640 + i * 100, 687.5)
            if i < 1:
                BP_re_1 = M_Taper_3.rotated(degrees=90).translated(4640 + i * 100, 630)
                insts += BP_re_1, f"re_pad_taper_{i}"
            else:
                BP_re_2 = M_Taper_3.rotated(degrees=90).translated(4640 + i * 100, 630)
                insts += BP_re_2, f"re_pad_taper_{i}"
            insts += BP_re, f"re_pad_{i}"
        tranceiver = cast(Mapping[str, fp.ICellRef], insts)
        # define ring filter position
        for i in range(N):
            for j in range(3):
                BP_rf = BondPad_100.translated(6248.6 - 150 + 10.5 + j * 150 + i * spacing, 694.125)
                BP_rf_taper = M_Taper_5.rotated(degrees=90).translated(6248.6 - 150 + 10.5 + j * 150 + i * spacing, 624.125)
                insts += BP_rf, f"rf_pad_{i}, {j}"
                insts += BP_rf_taper, f"rf_pad_taper{i}, {j}"
        tranceiver = cast(Mapping[str, fp.ICellRef], insts)
        # define ring filter middle pad opposite pad taper
        for i in range(N):
            BP_rf_taper_mirror = M_Taper_5.rotated(degrees=-90).translated(6248.6 + 10.5 + i * spacing,
                                                                           624.125-14.25)
            insts += BP_rf_taper_mirror, f"rf_pad_taper_mirror{i}, {j}"
        tranceiver = cast(Mapping[str, fp.ICellRef], insts)

        # additional M1/Via1 layer
        M1_10 = TECH.METAL.M1.W20.updated(line_width=10)
        for i in range(N):
            M1 = M1_10(
                curve=fp.g.Polyline(
                    [
                     # (3497.349 - i * spacing, 579.725),
                    (tranceiver["RM_3"]["ep_1"].position[0]- i * spacing, tranceiver["RM_3"]["ep_1"].position[1]-20),
                     (tranceiver["RM_3"]["ep_1"].position[0]- i * spacing, tranceiver["RM_3"]["ep_1"].position[1]+5-350)]

                )
            )
            VIA1 = fp.el.Rect(width=5, height=5, center=(tranceiver["RM_3"]["ep_1"].position[0] - i * spacing, tranceiver["RM_3"]["ep_1"].position[1]-20), layer=TECH.LAYER.VIA1_DRW)
            VIA2 = fp.el.Rect(width=5, height=5, center=(tranceiver["RM_3"]["ep_1"].position[0] - i * spacing, tranceiver["RM_3"]["ep_1"].position[1]+5-350+10), layer=TECH.LAYER.VIA1_DRW)
            insts += M1, f"M1_{i}"
            # elems += VIA1, f"via1_{i}"
            elems += VIA2, f"via2_{i}"
        tranceiver = cast(Mapping[str, fp.ICellRef], insts)

        MT_10 = TECH.METAL.MT.W10
        MT_20 = TECH.METAL.MT.W20

        MT = MT_20(
            curve=fp.g.Polyline(
                [
                    (tranceiver["tr_pad_0"]["ep_0"].position[0],tranceiver["tr_pad_0"]["ep_0"].position[1]),
                    (tranceiver["tr_pad_0"]["ep_0"].position[0],tranceiver["RM_3"]["ep_1"].position[1]+5-350+10),
                    (tranceiver["RM_3"]["ep_1"].position[0]+5,
                     tranceiver["RM_3"]["ep_1"].position[1] + 5 - 350+10)

        ]
            )
        )
        insts += MT
        #tr_metal_link
        for i in range(N):
            tr_metal_link = fp.LinkBetween(
                start=tranceiver[f"RM_{i}"]["ep_0"].with_orientation(degrees=-90),
                end=tranceiver[f"tr_pad_{8-i}"]["ep_0"].with_orientation(degrees=-90),
                metal_line_type=MT_10,
                min_distance=20,
                waylines=[fp.until_y(tranceiver[f"RM_{i}"]["ep_0"].position[1]-35-60*i)],
            )
            insts += tr_metal_link

        #pd_left_n_metal_link
        for i in range(N):
            pd_left_n_metal_link = fp.LinkBetween(
                start=tranceiver[f"PD_{i+4}"]["ep_0"].with_orientation(degrees=0),
                end=tranceiver[f"tr_pad_{1+i}"]["ep_0"].with_orientation(degrees=-90),
                metal_line_type=MT_20,
                min_distance=20
            )
            insts += pd_left_n_metal_link

        # pd_left_p_metal_link
        for i in range(N):
            if i == 0:
                pd_left_p_metal_link = fp.LinkBetween(
                    start=tranceiver[f"PD_{i+4}"]["ep_1"].with_orientation(degrees=-180),
                    end=tranceiver[f"tr_pad_0"]["ep_0"].with_orientation(degrees=-90),
                    metal_line_type=MT_20,
                    min_distance=20
                )
            else:
                pd_left_p_metal_link = fp.LinkBetween(
                    start=tranceiver[f"PD_{i + 4}"]["ep_1"].with_orientation(degrees=-180),
                    end=tranceiver[f"tr_pad_0"]["ep_0"].with_orientation(degrees=-90),
                    metal_line_type=MT_20,
                    min_distance=5,
                    # waylines=[fp.until_y(tranceiver[f"PD_{i + 4}"]["ep_1"].position[1]-109)],
                    waypoints=[
                        fp.Waypoint(
                            tranceiver[f"PD_{i + 4}"]["ep_1"].position[0]-50,
                            tranceiver[f"PD_{i + 4}"]["ep_1"].position[1]-109.6,
                            -180
                        )
                    ]
                )
            insts += pd_left_p_metal_link

        # rm_pad_link middle
        for i in range(N):
            rm_pad1_link = fp.LinkBetween(
                start=tranceiver[f"rm_pad_{N-1-i}, 1"]["ep_0"].with_orientation(degrees=-90),
                end=tranceiver[f"RM_{i}"]["ep_3"].with_orientation(degrees=90),
                min_distance=5,
                metal_line_type=MT_10
            )
            insts += rm_pad1_link

        # rm_pad_link left
        for i in range(N):
            rm_pad0_link = fp.LinkBetween(
                start=tranceiver[f"rm_pad_{N-1-i}, 0"]["ep_0"].with_orientation(degrees=-90),
                end=tranceiver[f"RM_{i}"]["ep_2"].with_orientation(degrees=180),
                min_distance=5,
                metal_line_type=MT_10
            )
            insts += rm_pad0_link

        # rm_pad_link right
        for i in range(N):
            rm_pad2_link = fp.LinkBetween(
                start=tranceiver[f"rm_pad_{N-1-i}, 2"]["ep_0"].with_orientation(degrees=-90),
                end=tranceiver[f"RM_{i}"]["ep_2"].with_orientation(degrees=0),
                min_distance=5,
                metal_line_type=MT_10
            )
            insts += rm_pad2_link

        # rm_ep1_link
        for i in range(N):
            rm_ep1_link = fp.LinkBetween(
                start=tranceiver[f"RM_{i}"]["ep_1"].with_orientation(degrees=-90),
                end=tranceiver[f"M1_{N-1-i}"]["ep_0"].with_orientation(degrees=90),
                min_distance=5,
                metal_line_type=MT_10
            )
            insts += rm_ep1_link

        # pd_right_pad_link
        for i in range(N):
            pd_right_pad_link = fp.LinkBetween(
                start=tranceiver[f"rf_pad_{i}, 0"]["ep_0"].with_orientation(degrees=-90),
                end=tranceiver[f"rf_pad_{i}, 2"]["ep_0"].with_orientation(degrees=-90),
                min_distance=5,
                metal_line_type=MT_20,
                waylines=[fp.until_y(tranceiver[f"rf_pad_{i}, 0"]["ep_0"].position[1]-105)]
            )
            insts += pd_right_pad_link

        # rf_ep1_link
        for i in range(N):
            rf_ep1_link = fp.LinkBetween(
                start=tranceiver[f"re_pad_0"]["ep_0"].with_orientation(degrees=-90),
                end=tranceiver[f"RF_{i}"]["ep_1"].with_orientation(degrees=-90),
                min_distance=100,
                metal_line_type=MT_10

            )
            insts += rf_ep1_link

        # rf_ep0_link
        for i in range(N):
            rf_ep0_link = fp.LinkBetween(
                start=tranceiver[f"re_pad_{i+1}"]["ep_0"].with_orientation(degrees=-90),
                end=tranceiver[f"RF_{N-1-i}"]["ep_0"].with_orientation(degrees=-180),
                min_distance=50,
                metal_line_type=MT_10,
                waylines=[fp.until_y(tranceiver[f"RF_{N-1-i}"]["ep_0"].position[1]+50*i)],

            )
            insts += rf_ep0_link

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off
    radius = 10

    library += Transceiver()
    library += Transceiver(name="-10%", radius=radius*0.9)
    library += Transceiver(name="+10%", radius=radius*1.1)

    # fmt: on
    # =============================================================
    from gpdk.components import all as components

    fp.export_gds(library, file=gds_file)
    fp.plot(library)