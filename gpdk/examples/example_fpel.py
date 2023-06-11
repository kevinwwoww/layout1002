import math
from dataclasses import dataclass
from typing import Tuple
from gpdk.technology import get_technology, WG
from fnpcell import all as fp
from gpdk import all as pdk
import gpdk

@dataclass(eq=False)
class fpel(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        rect = fp.el.Rect(width=10, height=10, center=(0, 0), layer=TECH.LAYER.FWG_COR)
        rect2 = fp.el.Rect(width=8, height=8, center=(10, 0), layer=TECH.LAYER.M1_DRW, corner_radius=2)
        # elems += rect, rect2

        circle = fp.el.Circle(radius=10, origin=(0, 0), initial_degrees=30, final_degrees=90, layer=TECH.LAYER.M1_DRW)
        circle2 = fp.el.Circle(radius=8, origin=(15, 0), initial_degrees=0, final_degrees=120, layer=TECH.LAYER.N_DRW)

        # elems += circle, circle2

        poly = fp.el.Polygon(raw_shape=[(0, 0), (6, 2), (7, 8), (2, 12)], origin=(0, 0), layer=TECH.LAYER.M2_DRW)
        poly2 = fp.el.Polygon(raw_shape=[(3, 5), (6, 9), (11, 15), (4, 12)], origin=(10, 0), layer=TECH.LAYER.GE_DRW)

        # elems += poly, poly2

        ring = fp.el.Ring(outer_radius=5, inner_radius=2, initial_degrees=30, final_degrees=120, layer=TECH.LAYER.TIN_DRW)
        ring2 = fp.el.Ring(outer_radius=8, inner_radius=3, initial_degrees=0, final_degrees=90, origin=(10, 0), layer=TECH.LAYER.PINREC_TEXT)

        # elems += ring, ring2

        regpol = fp.el.RegularPolygon(sides=3, side_length=5, layer=TECH.LAYER.IOPORT_EREC)
        regpol2 = fp.el.RegularPolygon(sides=5, side_length=7, origin=(10, 0), layer=TECH.LAYER.PASS_MT)

        # elems += regpol, regpol2

        line = fp.el.Line(length=10, stroke_width=5, final_stroke_width=8, layer=TECH.LAYER.NP_DRW)
        line2 = fp.el.Line(length=10, stroke_width=3, final_stroke_width=5, stroke_offset=2, final_stroke_offset=5, anchor=fp.Anchor.CENTER, origin=(0, 5), layer=TECH.LAYER.PP_DRW)

        # elems += line, line2

        from gpdk.technology.font.font_std_vented import FONT as font
        label = fp.el.Label(content="LDA", highlight=True, at=(0, 0), font=font, font_size=10, layer=TECH.LAYER.LABEL_DRW)
        label2 = fp.el.Label(content="PHOTOCAD", highlight=False, at=(0, 12), font=font, font_size=15, layer=TECH.LAYER.TEXT_NOTE)
        # 
        elems += label, label2
        






        return insts, elems, ports




if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += fpel()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
