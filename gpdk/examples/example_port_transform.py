from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class PortTransform(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        # fmt: off
        TECH = get_technology()

        bend_bezier0 = pdk.BendBezier(start=(0, 0), controls=[(30, 30)], end=(60, 0), waveguide_type=TECH.WG.FWG.C.WIRE)

        insts += bend_bezier0
        bend_repositioned = bend_bezier0['op_1'].repositioned(at=bend_bezier0["op_0"]).owner
        insts += bend_repositioned

        bend_bezier = bend_bezier0.translated(0, 100)
        insts += bend_bezier
        bend_rotated = bend_bezier['op_1'].rotated(degrees=60).owner
        insts += bend_rotated

        bend_bezier = bend_bezier0.translated(100, 0)
        insts += bend_bezier
        bend_h = bend_bezier['op_1'].h_mirrored().owner
        insts += bend_h

        bend_bezier = bend_bezier0.translated(100, 100)
        insts += bend_bezier
        bend_v = bend_bezier['op_1'].v_mirrored().owner
        insts += bend_v

        bend_bezier = bend_bezier0.translated(0, 200)
        insts += bend_bezier
        bend_c = bend_bezier['op_1'].c_mirrored().owner
        insts += bend_c

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += PortTransform()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
