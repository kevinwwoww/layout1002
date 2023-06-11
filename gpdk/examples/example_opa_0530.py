import math
from dataclasses import dataclass
from typing import Tuple
from gpdk.technology import get_technology, WG
from fnpcell import all as fp
from gpdk import all as pdk
import gpdk
from gpdk.technology.waveguide_factory import CircularBendFactory

@dataclass(eq=False)
class MMI(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        layer = TECH.LAYER.FWG_COR
        mid_rec = fp.el.Rect(width=23, height=6, layer=layer, bottom_left=(0, 0))
        left_rec = fp.el.Rect(width=5, height=1.8, layer=layer, bottom_left=(-5, 2.1))
        right_rec_top = fp.el.Line(length=4, stroke_width=2.5, final_stroke_width=1.8, layer=layer, origin=(25, 4.75),
                                   anchor=fp.Anchor.CENTER)
        right_rec_bot = fp.el.Line(length=4, stroke_width=2.5, final_stroke_width=1.8, layer=layer, origin=(25, 1.25),
                                   anchor=fp.Anchor.CENTER)

        insts += mid_rec, left_rec, right_rec_top, right_rec_bot

        waveguide_type = TECH.WG.CHANNEL.C.WIRE.updated(wg_design_width=1.8)
        left_port = fp.Port(
            name="op_0",
            position=(-5, 3),
            waveguide_type=waveguide_type,
            orientation=-math.pi
        )
        right_top_port = fp.Port(
            name="op_1",
            position=(27, 4.75),
            waveguide_type=waveguide_type,
            orientation=0
        )
        right_bot_port = fp.Port(
            name="op_2",
            position=(27, 1.25),
            waveguide_type=waveguide_type,
            orientation=0
        )

        ports += left_port, right_top_port, right_bot_port

        return insts, elems, ports

@dataclass(eq=False)
class Taper(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        layer = TECH.LAYER.FWG_COR

        taper = fp.el.Line(length=2938.28, stroke_width=0.4, final_stroke_width=1.8, layer=layer, origin=(0, 0),
                                   anchor=fp.Anchor.START)

        insts += taper

        waveguide_type_start = TECH.WG.CHANNEL.C.WIRE.updated(wg_design_width=0.4)
        waveguide_type_end = TECH.WG.CHANNEL.C.WIRE.updated(wg_design_width=1.8)
        left_port = fp.Port(
            name="op_0",
            position=(0, 0),
            waveguide_type=waveguide_type_start,
            orientation=-math.pi
        )
        right_port = fp.Port(
            name="op_1",
            position=(2938.28, 0),
            waveguide_type=waveguide_type_end,
            orientation=0
        )


        ports += left_port, right_port

        return insts, elems, ports

@dataclass(eq=False)
class Bragg(fp.PCell):

    period: float = fp.PositiveFloatParam(default=1.2)
    
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        period = self.period

        layer = TECH.LAYER.FWG_COR

        start_straight = fp.el.Rect(width=30, height=1.8, layer=layer, bottom_left=(0, 0))
        start_bragg = fp.el.Rect(width=0.9, height=1.8, layer=layer, bottom_left=(30, 0))
        for i in range(58):
            small_rect = fp.el.Rect(width=period / 2, height=0.9, layer=layer, bottom_left=(30.9 + period * i , 0.45))
            big_rect = fp.el.Rect(width=period / 2, height=1.8, layer=layer, bottom_left=(30.9 + period / 2 + period * i , 0))

            insts += small_rect, big_rect

        end_straight = fp.el.Rect(width=3600.5 - (30.9 + 58 * period) , height=1.8, layer=layer, bottom_left=(30.9 + 58 * period, 0))


        insts += start_straight, start_bragg, end_straight

        waveguide_type = TECH.WG.CHANNEL.C.WIRE.updated(wg_design_width=1.8)
        left_port = fp.Port(
            name="op_0",
            position=(0, 0.9),
            waveguide_type=waveguide_type,
            orientation=-math.pi
        )
        right_port = fp.Port(
            name="op_1",
            position=(3600.5, 0.9),
            waveguide_type=waveguide_type,
            orientation=0
        )
        ports += left_port, right_port

        return insts, elems, ports

@dataclass(eq=False)
class MMI_tree(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        taper = Taper()
        mmi1 = MMI().translated(0, 0)
        mmi2 = MMI().translated(210, 75)
        mmi3 = MMI().translated(210, -75)
        mmi4 = MMI().translated(210+120, 75+30)
        mmi5 = MMI().translated(210+120, 75-30)
        mmi6 = MMI().translated(210+120, -75+30)
        mmi7 = MMI().translated(210+120, -75-30)

        mmi8 = MMI().translated(210+120+90, 75+30+14)
        mmi9 = MMI().translated(210+120+90, 75+30-14)
        mmi10 = MMI().translated(210+120+90, 75-30+14)
        mmi11 = MMI().translated(210+120+90, 75-30-14)

        mmi12 = MMI().translated(210+120+90, -75+30+14)
        mmi13 = MMI().translated(210+120+90, -75+30-14)
        mmi14 = MMI().translated(210+120+90, -75-30+14)
        mmi15 = MMI().translated(210+120+90, -75-30-14)

        insts += mmi1, mmi2, mmi3, mmi4, mmi5, mmi6, mmi7, mmi8, mmi9, mmi10, mmi11, mmi12, mmi13, mmi14, mmi15


        bend_factory1 = CircularBendFactory(radius_eff=125, waveguide_type=TECH.WG.CHANNEL.C.WIRE)
        link1 = fp.create_links(
            link_type=TECH.WG.CHANNEL.C.WIRE,
            bend_factory=bend_factory1,
            specs=[
                fp.LinkBetween(
                    start=mmi1["op_1"],
                    end=mmi2["op_0"]
                ),
                fp.LinkBetween(
                    start=mmi1["op_2"],
                    end=mmi3["op_0"]
                )
            ]
        )

        bend_factory2 = CircularBendFactory(radius_eff=75.5, waveguide_type=TECH.WG.CHANNEL.C.WIRE)
        link2 = fp.create_links(
            link_type=TECH.WG.CHANNEL.C.WIRE,
            bend_factory=bend_factory2,
            specs=[
                fp.LinkBetween(
                    start=mmi2["op_1"],
                    end=mmi4["op_0"]
                ),
                fp.LinkBetween(
                    start=mmi2["op_2"],
                    end=mmi5["op_0"]
                ),
                fp.LinkBetween(
                    start=mmi3["op_1"],
                    end=mmi6["op_0"]
                ),
                fp.LinkBetween(
                    start=mmi3["op_2"],
                    end=mmi7["op_0"]
                )
            ]
        )

        bend_factory3 = CircularBendFactory(radius_eff=71.5, waveguide_type=TECH.WG.CHANNEL.C.WIRE)
        link3 = fp.create_links(
            link_type=TECH.WG.CHANNEL.C.WIRE,
            bend_factory=bend_factory3,
            specs=[
                fp.LinkBetween(
                    start=mmi4["op_1"],
                    end=mmi8["op_0"]
                ),
                fp.LinkBetween(
                    start=mmi4["op_2"],
                    end=mmi9["op_0"]
                ),
                fp.LinkBetween(
                    start=mmi5["op_1"],
                    end=mmi10["op_0"]
                ),
                fp.LinkBetween(
                    start=mmi5["op_2"],
                    end=mmi11["op_0"]
                ),
                fp.LinkBetween(
                    start=mmi6["op_1"],
                    end=mmi12["op_0"]
                ),
                fp.LinkBetween(
                    start=mmi6["op_2"],
                    end=mmi13["op_0"]
                ),
                fp.LinkBetween(
                    start=mmi7["op_1"],
                    end=mmi14["op_0"]
                ),
                fp.LinkBetween(
                    start=mmi7["op_2"],
                    end=mmi15["op_0"]
                ),
            ]
        )


        insts += link1, link2, link3

        ports += mmi1["op_0"].with_name("op_0")
        ports += mmi8["op_1"].with_name("op_1")
        ports += mmi8["op_2"].with_name("op_2")
        ports += mmi9["op_1"].with_name("op_3")
        ports += mmi9["op_2"].with_name("op_4")
        ports += mmi10["op_1"].with_name("op_5")
        ports += mmi10["op_2"].with_name("op_6")
        ports += mmi11["op_1"].with_name("op_7")
        ports += mmi11["op_2"].with_name("op_8")
        ports += mmi12["op_1"].with_name("op_9")
        ports += mmi12["op_2"].with_name("op_10")
        ports += mmi13["op_1"].with_name("op_11")
        ports += mmi13["op_2"].with_name("op_12")
        ports += mmi14["op_1"].with_name("op_13")
        ports += mmi14["op_2"].with_name("op_14")
        ports += mmi15["op_1"].with_name("op_15")
        ports += mmi15["op_2"].with_name("op_16")

        return insts, elems, ports

@dataclass(eq=False)
class OPA(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        mmi_tree = MMI_tree()
        taper = Taper()
        bragg = Bragg()
        bragg1 = Bragg(period=1.0)

        mmi_tree = mmi_tree.translated(0, 0)
        taper = taper["op_1"].repositioned(at=(mmi_tree["op_0"].position[0],mmi_tree["op_0"].position[1])).owner

        mmi_taper_link = fp.create_links(
            link_type=TECH.WG.CHANNEL.C.WIRE,
            bend_factory=TECH.WG.CHANNEL.C.WIRE.BEND_CIRCULAR,
            specs=[
                fp.LinkBetween(
                    start=taper["op_1"],
                    end=mmi_tree["op_0"],
                )
            ]
        )

        insts += taper, mmi_tree, mmi_taper_link

        for i in range(4):
            bragg_top = bragg["op_0"].repositioned(at=(mmi_tree[f"op_{ 2*i + 1}"].position[0] + 40 ,mmi_tree[f"op_{2*i + 1}"].position[1] + 5)).owner

            link_top = fp.create_links(
                link_type=TECH.WG.CHANNEL.C.WIRE,
                bend_factory=CircularBendFactory(radius_eff=80, waveguide_type=TECH.WG.CHANNEL.C.WIRE),
                specs=[
                    fp.LinkBetween(
                        start=bragg_top["op_0"],
                        end=mmi_tree[f"op_{ 2*i + 1}"]

                    )
                ]
            )

            insts += bragg_top, link_top

        for i in range(1, 5):
            bragg_bot = bragg["op_0"].repositioned(at=(mmi_tree[f"op_{ 2*i}"].position[0] + 40 ,mmi_tree[f"op_{2*i}"].position[1] - 5)).owner

            link_bot = fp.create_links(
                link_type=TECH.WG.CHANNEL.C.WIRE,
                bend_factory=CircularBendFactory(radius_eff=80, waveguide_type=TECH.WG.CHANNEL.C.WIRE),
                specs=[
                    fp.LinkBetween(
                        start=bragg_bot["op_0"],
                        end=mmi_tree[f"op_{ 2*i}"]

                    )
                ]
            )

            insts += bragg_bot, link_bot

        for i in range(4, 8):
            bragg_top = bragg1["op_0"].repositioned(at=(mmi_tree[f"op_{ 2*i + 1}"].position[0] + 40 ,mmi_tree[f"op_{2*i + 1}"].position[1] + 5)).owner

            link_top = fp.create_links(
                link_type=TECH.WG.CHANNEL.C.WIRE,
                bend_factory=CircularBendFactory(radius_eff=80, waveguide_type=TECH.WG.CHANNEL.C.WIRE),
                specs=[
                    fp.LinkBetween(
                        start=bragg_top["op_0"],
                        end=mmi_tree[f"op_{ 2*i + 1}"]

                    )
                ]
            )

            insts += bragg_top, link_top

        for i in range(5, 9):
            bragg_bot = bragg1["op_0"].repositioned(at=(mmi_tree[f"op_{ 2*i}"].position[0] + 40 ,mmi_tree[f"op_{2*i}"].position[1] - 5)).owner

            link_bot = fp.create_links(
                link_type=TECH.WG.CHANNEL.C.WIRE,
                bend_factory=CircularBendFactory(radius_eff=80, waveguide_type=TECH.WG.CHANNEL.C.WIRE),
                specs=[
                    fp.LinkBetween(
                        start=bragg_bot["op_0"],
                        end=mmi_tree[f"op_{ 2*i}"]

                    )
                ]
            )

            insts += bragg_bot, link_bot

        for i in range(3):
            triangle = fp.el.Polygon(
                raw_shape= [(0, 0), (40, 0), (20, 60)],
                layer=TECH.LAYER.FWG_COR,
                origin=(0, 0)
            )
            left_triangle = triangle.translated(-2943.38 + 274 + 50 * i, 2.8 + 24)

            elems += left_triangle

            right_triangle = triangle.translated(3101 + 50 * i, 2.8 - 271)

            elems += right_triangle


        return insts, elems, ports

if __name__ == "__main__":
    from gpdk.components import all as components
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += MMI_tree()
    library += Taper()
    library += OPA()
    library += Bragg1_0()


    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)


    # fp.plot(library)


        

