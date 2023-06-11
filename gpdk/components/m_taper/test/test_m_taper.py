from fnpcell import all as fp
from gpdk.components.m_taper.m_taper import MTaper
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_m_taper():
    library = fp.Library()

    # =======================================================================
    # fmt: off

    library += MTaper(final_offset=27)

    # fmt: on
    # =============================================================
    return library
