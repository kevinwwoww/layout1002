from fnpcell import all as fp
from gpdk.components.spiral.spiral import Spiral
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_spiral():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += Spiral(total_length=2000, n_o_loops=6, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    # fp.plot(library)

    return library


if __name__ == "__main__":
    test_spiral()
