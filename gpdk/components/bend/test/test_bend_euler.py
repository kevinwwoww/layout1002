from fnpcell import all as fp
from gpdk.components.bend.bend_euler import BendEuler
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


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
