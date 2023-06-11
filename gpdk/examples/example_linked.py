from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.technology.waveguide_factory import EulerBendFactory


@dataclass(eq=False)
class Linked(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off

        sbend = pdk.SBend(distance=100, height=-90, waveguide_type=TECH.WG.FWG.C.WIRE, bend_factory=EulerBendFactory(radius_min=15, l_max=35, waveguide_type=TECH.WG.FWG.C.WIRE))
        straight_fw = pdk.Straight(length=5, waveguide_type=TECH.WG.FWG.C.WIRE)
        straight_fe = pdk.Straight(length=5, waveguide_type=TECH.WG.FWG.C.EXPANDED)
        straight_mw = pdk.Straight(length=5, waveguide_type=TECH.WG.MWG.C.WIRE)
        straight_sw = pdk.Straight(length=5, waveguide_type=TECH.WG.SWG.C.WIRE)

        sb10 = sbend.translated(-200, 0)
        s10 = straight_fw
        s15 = straight_fe.translated(100, 0)
        s20 = straight_sw.translated(200, 0)
        s30 = straight_mw.rotated(degrees=30).translated(300, 100)
        s40 = straight_fw.rotated(degrees=30).translated(50, 100)

        # #  fp.plot(fp.Library(sb10,s10,s15,s20,s30,s40))

        # bend_factory = EulerBendFactory(radius_min=15, l_max=15, waveguide_type=TECH.WG.SWG.C.WIRE)
        device = fp.Linked(
            link_type=TECH.WG.SWG.C.EXPANDED,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER, #bend_factory,
            links=[
                sb10["op_1"] >> s10["op_0"],
                s10["op_1"] >> s15["op_0"],
                s15["op_1"] >> s20["op_0"],
                s20["op_1"] >> s30["op_0"],
                s30["op_1"] >> s40["op_0"],
            ],
            ports=[sb10["op_0"], s40["op_1"]],
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

    library += Linked()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
