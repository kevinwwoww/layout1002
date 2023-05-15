from fnpcell import all as fp
from fpdk.components.combiner.y_combiner import YCombiner
from fpdk.technology import get_technology
from fpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_y_combiner():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += YCombiner(waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    return library
