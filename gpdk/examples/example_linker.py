from dataclasses import dataclass

from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.technology.waveguide_factory import EulerBendFactory


@dataclass(eq=False)
class LinkBetweenInLinked(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        bend_factory_15_35 = EulerBendFactory(radius_min=15, l_max=35, waveguide_type=TECH.WG.FWG.C.WIRE)

        sbend = pdk.SBend(distance=100, height=-90, waveguide_type=TECH.WG.FWG.C.WIRE, bend_factory=bend_factory_15_35)
        straight_fw = pdk.Straight(length=5, waveguide_type=TECH.WG.FWG.C.WIRE)
        straight_fe = pdk.Straight(length=5, waveguide_type=TECH.WG.FWG.C.EXPANDED)
        straight_mw = pdk.Straight(length=5, waveguide_type=TECH.WG.MWG.C.WIRE)
        straight_sw = pdk.Straight(length=5, waveguide_type=TECH.WG.SWG.C.WIRE)

        sb10 = sbend.translated(-200, 0)
        s10 = straight_fw
        s15 = straight_fe.translated(100, 0)
        s20 = straight_sw.translated(200, 0)
        s30 = straight_mw.rotated(degrees=30).translated(400, 200)
        s40 = straight_fw.rotated(degrees=30).translated(50, 100)

        # #  fp.plot(fp.Library(sb10,s10,s15,s20,s30,s40))

        bend_factory_15_5 = EulerBendFactory(radius_min=15, l_max=5, waveguide_type=TECH.WG.SWG.C.WIRE)
        bend_factory_50_5 = EulerBendFactory(radius_min=50, l_max=5, waveguide_type=TECH.WG.MWG.C.WIRE)

        device = fp.Linked(
            link_type=TECH.WG.SWG.C.EXPANDED,
            bend_factory=bend_factory_15_5,
            links=[
                sb10["op_1"] >> s10["op_0"],
                s10["op_1"] >> s15["op_0"],
                s15["op_1"] >> s20["op_0"],
                fp.LinkBetween(start=s20["op_1"], end=s30["op_0"], bend_factory=bend_factory_50_5),
                TECH.LINKER.SWG_EXPANDED_MWG_EULER(
                    start=s30["op_1"],
                    end=s40["op_0"],
                    waylines=[
                        fp.until_x(fp.PREV + 50),
                        fp.until_y(fp.PREV + 30),
                        fp.until_x(200),
                        fp.until_y(150),
                        fp.until_x(150),
                    ],
                ),
            ],
            ports=[],  # [sb10["op_0"], s40["op_1"]],
        )
        insts += device

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.components import all as components
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================

    library += LinkBetweenInLinked()

    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=components)
    # fp.plot(library)
