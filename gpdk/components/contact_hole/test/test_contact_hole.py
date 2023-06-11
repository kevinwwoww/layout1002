from fnpcell import all as fp
from gpdk.components.contact_hole.contact_hole import ContactHole
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_contact_hole():
    library = fp.Library()

    # =======================================================================
    # fmt: off

    library += ContactHole(name="d", num_sides=4, top_width=2, bottom_width=1.6, via_width=0.4)

    # fmt: on
    # =============================================================
    return library
