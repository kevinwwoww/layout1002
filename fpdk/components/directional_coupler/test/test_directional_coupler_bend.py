from fnpcell import all as fp
from fpdk.components.directional_coupler.directional_coupler_bend import DirectionalCouplerBend
from fpdk.technology import get_technology
from fpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_directional_coupler_bend():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += DirectionalCouplerBend(name="f", coupler_spacing=0.7, coupler_length=6, bend_radius=10, straight_after_bend=6, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    return library
