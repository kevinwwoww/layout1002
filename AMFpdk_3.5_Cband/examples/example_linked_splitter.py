from dataclasses import dataclass
from fnpcell import all as fp
from AMFpdk_3_5_Cband import all as pdk
from AMFpdk_3_5_Cband.technology import get_technology

@fp.pcell_class()
@dataclass(eq=False)
class LinkedSplitter(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        Y1 = pdk.YSplitter(waveguide_type=TECH.WG.RIB.C.WIRE, taper_length=40, bend_radius=90)
        Y2 = pdk.YSplitter(waveguide_type=TECH.WG.RIB.C.WIRE, taper_length=40, bend_radius=90,
                           transform=fp.rotate(degrees=180))

        YSplitter1 = Y1.translated(-150, 0)
        YSplitter2 = Y2.translated(150, 0)

        device = fp.Linked(
            link_type=TECH.WG.GRAT.C.WIRE,
            bend_factory=TECH.WG.RIB.C.WIRE.BEND_EULER,
            links=[
                YSplitter1["op_1"] >> YSplitter2["op_2"],
                YSplitter1["op_2"] >> YSplitter2["op_1"],
            ],
            ports=[],
        )

        insts += device

        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk_3_5_Cband.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += LinkedSplitter()

    fp.export_gds(library, file=gds_file)
