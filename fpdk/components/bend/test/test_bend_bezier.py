from fnpcell import all as fp
from fpdk.components.bend.bend_bezier import BendBezier
from fpdk.technology import get_technology
from fpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_bend_bezier():
    library = fp.Library()
    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += BendBezier(name="q", start=(0, 0), controls=[(31, 30)], end=(60, 0), waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================

    return library
