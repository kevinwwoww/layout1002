from fnpcell import all as fp
from gpdk.components.bend.bend_circular import BendCircular
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_bend_circular():
    library = fp.Library()
    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += BendCircular(name="s", radius=5, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    # fp.plot(library)
    return library
