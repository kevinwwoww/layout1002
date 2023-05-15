from fnpcell import all as fp
from fpdk.components.directional_coupler.directional_coupler_half_ring import DCHalfRingStraight
from fpdk.technology import get_technology
from fpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_directional_coupler_half_ring():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += DCHalfRingStraight(name="f", coupler_length=0, coupler_spacing=0.2, bend_radius=10,waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    return library
