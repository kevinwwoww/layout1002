from dataclasses import dataclass
from fnpcell import all as fp
from IMECAS_pdk import all as pdk
from IMECAS_pdk.technology import get_technology
import IMECAS_pdk
from IMECAS_pdk.technology.font.font_std_vented import FONT as font_gds

@dataclass(eq=False)
class AWG(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        awg = pdk.AWG200G_C_TE_8ch_WG450()
        gc = pdk.FGC_C_TE_WG450()

        left_awg = awg.translated(100, 0)
        left_gc = gc
        left_gc = left_gc["out_0"].repositioned(at=(-100, left_awg["in0"].position[1])).owner
        right_gc_1 = gc.h_mirrored().translated(1100, 422)
        right_gc_2 = gc.h_mirrored().translated(1100, 342)
        right_gc_3 = gc.h_mirrored().translated(1100, 262)
        right_gc_4 = gc.h_mirrored().translated(1100, 182)
        right_gc_5 = gc.h_mirrored().translated(1100, 102)
        right_gc_6 = gc.h_mirrored().translated(1100, 22)
        right_gc_7 = gc.h_mirrored().translated(1100, -58)
        right_gc_8 = gc.h_mirrored().translated(1100, -138)


        link1 = fp.create_links(
            link_type=TECH.WG.Channel.C.WIRE,
            bend_factory=TECH.WG.Channel.C.WIRE.BEND,
            specs=[
                fp.LinkBetween(
                    start=left_gc["out_0"],
                    end=left_awg["in0"]
                )
            ]
        )

        link2 = fp.create_links(
            link_type=TECH.WG.Channel.C.WIRE,
            bend_factory=TECH.WG.Channel.C.WIRE.BEND,
            specs=[
                fp.LinkBetween(
                    start=right_gc_1["out_0"],
                    end=left_awg["out1"]
                ),
                fp.LinkBetween(
                    start=right_gc_2["out_0"],
                    end=left_awg["out2"],
                    waypoints=[fp.Waypoint(
                        left_awg["out2"].position[0] + 50,
                        left_awg["out2"].position[1],
                        180)
                    ]
                ),
                fp.LinkBetween(
                    start=right_gc_3["out_0"],
                    end=left_awg["out3"],
                    waypoints=[fp.Waypoint(
                        left_awg["out3"].position[0] + 100,
                        left_awg["out3"].position[1],
                        180)
                    ]
                ),
                fp.LinkBetween(
                    start=right_gc_4["out_0"],
                    end=left_awg["out4"],
                    waypoints=[fp.Waypoint(
                        left_awg["out4"].position[0] + 150,
                        left_awg["out4"].position[1],
                        180)
                    ]
                ),
                fp.LinkBetween(
                    start=right_gc_5["out_0"],
                    end=left_awg["out5"]
                ),
                fp.LinkBetween(
                    start=right_gc_6["out_0"],
                    end=left_awg["out6"],
                    waypoints=[fp.Waypoint(
                        left_awg["out6"].position[0] + 150,
                        left_awg["out6"].position[1],
                        180)
                    ]
                ),
                fp.LinkBetween(
                    start=right_gc_7["out_0"],
                    end=left_awg["out7"],
                    waypoints=[fp.Waypoint(
                        left_awg["out7"].position[0] + 100,
                        left_awg["out7"].position[1],
                        180)
                    ]
                ),
                fp.LinkBetween(
                    start=right_gc_8["out_0"],
                    end=left_awg["out8"],
                    waypoints=[fp.Waypoint(
                        left_awg["out8"].position[0] + 50,
                        left_awg["out8"].position[1],
                        180)
                    ]
                )
            ]
        )

        awg_label = fp.el.Label(content="AWG200G_C_TE_8CH_WG450", layer=TECH.LAYER.DOC, at=(100, -50), font_size=25, font=font_gds)
        logo = fp.el.Label(content="LATITUDE DESIGN AUTOMATION", layer=TECH.LAYER.DOC, at=(660, -180), font_size=20, font=font_gds)

        elems += awg_label, logo




        insts += left_awg, left_gc, link1, link2
        insts += right_gc_1, right_gc_2, right_gc_3, right_gc_4, right_gc_5, right_gc_6, right_gc_8, right_gc_7
        return insts, elems, ports


if __name__ == "__main__":
    from IMECAS_pdk.components import all as components
    from IMECAS_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += AWG()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)

    # fp.plot(library)