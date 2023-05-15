from fnpcell import all as fp
from fpdk.components import all as pdk
from fpdk.technology import get_technology
from fpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_taper_parabolic():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    swg_update = TECH.WG.SWG.C.WIRE.updated(core_design_width=3.8, cladding_design_width=9.6)
    library += pdk.TaperParabolic(name="a", length=20, left_type=swg_update, right_type=TECH.WG.SWG.C.WIRE)

    # fmt: on
    # =============================================================
    return library
