from dataclasses import dataclass

from fnpcell import all as fp
from IMECAS_SiN_pdk_1_0_0 import all as pdk
from IMECAS_SiN_pdk_1_0_0.technology import get_technology
from IMECAS_SiN_pdk_1_0_0.technology.waveguide_factory import bb_C_BendFactory


TECH = get_technology()


@dataclass(eq=False)
class MMItest(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        mmi = pdk.SIN_MMI1X2_C()
        gc = pdk.SIN_FGC_TE_C()

        left_gc = gc.translated(0, -500)
        right_gc_1 = gc.h_mirrored().translated(5000, 401)
        right_gc_2 = gc.h_mirrored().translated(5000, 0)
        right_gc_3 = gc.h_mirrored().translated(5000, -300)
        right_gc_4 = gc.h_mirrored().translated(5000, -600)
        right_gc_5 = gc.h_mirrored().translated(5000, -1200)

        mmi_1 = mmi.translated(1000, 0)
        mmi_2 = mmi.translated(2000, -300)
        mmi_3 = mmi.translated(3000, -600)
        mmi_4 = mmi.translated(4000, -900)

        bend = bb_C_BendFactory(waveguide_type=TECH.WG.Channel.C.WIRE)

        device = fp.Linked(
            link_type=TECH.WG.Channel.C.WIRE,
            # bend_factory=TECH.WG.Channel.O.WIRE.BEND,
            bend_factory=bend,
            links=[
                # left_gc["out1"] >> mmi_1["in1"],
                right_gc_1["out1"] >> mmi_1["out1"],
                # mmi_1["out2"] >> mmi_2["in1"],
                # right_gc_2["out1"] >> mmi_2["out1"],
                # mmi_2["out2"] >> mmi_3["in1"],
                # right_gc_3["out1"] >> mmi_3["out1"],
                # mmi_3["out2"] >> mmi_4["in1"],
                # right_gc_4["out1"] >> mmi_4["out1"],
                # right_gc_5["out1"] >> mmi_4["out2"],
            ],
            ports=[],
        )

        insts += device

        return insts, elems, ports


if __name__ == "__main__":
    from IMECAS_SiN_pdk_1_0_0.components import all as components
    from IMECAS_SiN_pdk_1_0_0.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += MMItest()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)

    fp.plot(library)

