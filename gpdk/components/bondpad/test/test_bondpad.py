from fnpcell import all as fp
from gpdk.components.bondpad.bondpad import BondPad
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_bondpad():
    library = fp.Library()

    # =======================================================================
    # fmt: off

    library += BondPad(pad_width=75, pad_height=75)

    # fmt: on
    # =============================================================
    return library
