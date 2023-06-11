from fnpcell import all as fp
from gpdk.components import all as pdk
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)  # (plot_differences=True)
def test_sbend():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += pdk.SBend(name="f", distance=100, height=90, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    # fp.plot(library)
    return library
