from fnpcell import all as fp
from gpdk.components.fixed_edge_coupler.fixed_edge_coupler import Fixed_Edge_Coupler
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_fixed_edge_coupler():
    library = fp.Library()

    # =======================================================================
    # fmt: off

    library += Fixed_Edge_Coupler()

    # fmt: on
    # =============================================================
    return library
