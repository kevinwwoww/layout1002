from fnpcell import all as fp
from gpdk.components import all as pdk
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_fwg2swg_transition():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += pdk.FWG2SWGTransition(name="a", length=20, fwg_type=TECH.WG.FWG.C.WIRE, swg_type=TECH.WG.SWG.C.WIRE, transform=fp.translate(0, 20))

    # fmt: on
    # =============================================================
    return library
