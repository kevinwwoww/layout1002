from fnpcell import all as fp
from gpdk.components.edge_coupler_1550.edge_coupler_1550 import Edge_Coupler_1550
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_edge_coupler_1550():
    library = fp.Library()

    # =======================================================================
    # fmt: off

    library += Edge_Coupler_1550()

    # fmt: on
    # =============================================================
    return library
