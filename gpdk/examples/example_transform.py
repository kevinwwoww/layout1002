from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class Transform(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        # fmt: off
        TECH = get_technology()

        bend_bezier = pdk.BendBezier(start=(0, 0), controls=[(30, 30)], end=(60, 0), waveguide_type=TECH.WG.FWG.C.WIRE)

        bend_translated = bend_bezier.translated(50, 50)
        insts += bend_translated
        bend_rotated = bend_bezier.rotated(degrees=60)
        insts += bend_rotated
        bend_h = bend_bezier.h_mirrored(x=0)
        insts += bend_h
        bend_v = bend_bezier.v_mirrored(y=0)
        insts += bend_v
        bend_c = bend_bezier.c_mirrored(center=(0, 0))
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

    library += Transform()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
