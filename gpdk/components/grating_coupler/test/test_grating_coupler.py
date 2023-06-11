from fnpcell import all as fp
from gpdk.components.grating_coupler.grating_coupler import GratingCoupler
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_grating_coupler():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += GratingCoupler(name="f", transform=fp.translate(0, 60), waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    # fp.plot(library)
    return library
