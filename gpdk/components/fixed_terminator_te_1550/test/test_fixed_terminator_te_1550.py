from fnpcell import all as fp
from gpdk.components.fixed_terminator_te_1550.fixed_terminator_te_1550 import Fixed_Terminator_TE_1550
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_fixed_terminator_te_1550():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += Fixed_Terminator_TE_1550(length=30, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    return library
