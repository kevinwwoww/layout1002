from dataclasses import dataclass
from fnpcell import all as fp
from IMECAS_pdk import all as pdk
from IMECAS_pdk.technology import get_technology
import IMECAS_pdk
from IMECAS_pdk.technology.font.font_std_vented import FONT as font_gds



@dataclass(eq=False)
class MMItest(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        mmi = pdk.MMI1X2_O_WG380()
        gc = pdk.FGC_O_TE_WG380()

        left_gc = gc.translated(-200, 100)
        right_gc_1 = gc.h_mirrored().translated(700, 0)
        right_gc_2 = gc.h_mirrored().translated(700, -50)
        right_gc_3 = gc.h_mirrored().translated(700, -100)
        right_gc_4 = gc.h_mirrored().translated(700, -150)
        right_gc_5 = gc.h_mirrored().translated(700, -200)

        mmi_1 = mmi.translated(100, 0)
        mmi_2 = mmi.translated(200, -50)
        mmi_3 = mmi.translated(300, -100)
        mmi_4 = mmi.translated(400, -150)

        device = fp.Linked(
            link_type=TECH.WG.Rib.O.WIRE,
            bend_factory=TECH.WG.Rib.O.WIRE.BEND,
            links=[
                left_gc["out_0"] >> mmi_1["input"],
                right_gc_1["out_0"] >> mmi_1["output2"],
                mmi_1["output1"] >> mmi_2["input"],
                right_gc_2["out_0"] >> mmi_2["output2"],
                mmi_2["output1"] >> mmi_3["input"],
                right_gc_3["out_0"] >> mmi_3["output2"],
                mmi_3["output1"] >> mmi_4["input"],
                right_gc_4["out_0"] >> mmi_4["output2"],
                right_gc_5["out_0"] >> mmi_4["output1"],
            ],
            ports=[],
        )
        logo = fp.el.Label(content="LATITUDE DESIGN AUTOMATION", layer=TECH.LAYER.DOC, at=(700-442.857, -240), font_size=20, font=font_gds)
        mmi = fp.el.Label(content="MMI1X2_O_WG380", layer=TECH.LAYER.DOC, at=(77, -130), font_size=15, font=font_gds)
        tran = fp.el.Label(content="TR380_RIB580", layer=TECH.LAYER.DOC, at=(77, -160), font_size=15, font=font_gds)
        elems += logo, mmi, tran

        insts += device

        return insts, elems, ports


if __name__ == "__main__":
    from IMECAS_pdk.components import all as components
    from IMECAS_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += MMItest()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)

    # fp.plot(library)
