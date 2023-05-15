from fnpcell import all as fp
from fpdk.components.bend.bend_euler import BendEuler
from fpdk.technology import get_technology
from fpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_bend_euler():
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += BendEuler(name="e60", radius_min=50, degrees=60, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    return library
