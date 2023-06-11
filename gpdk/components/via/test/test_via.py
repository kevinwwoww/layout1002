from fnpcell import all as fp
from gpdk.components import all as pdk
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_via():
    library = fp.Library()

    # =======================================================================
    # fmt: off

    library += pdk.Via(name="s")

    # fmt: on
    # =============================================================
    return library
