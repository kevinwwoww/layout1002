from fnpcell import all as fp
from gpdk.components import all as pdk
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_swg2mwg_transition():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += pdk.SWG2MWGTransition(name="a", swg_type=TECH.WG.SWG.C.WIRE, mwg_type=TECH.WG.MWG.C.WIRE, transform=fp.translate(0, 20))

    # fmt: on
    # =============================================================
    return library
