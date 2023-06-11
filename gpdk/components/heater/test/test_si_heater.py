from fnpcell import all as fp
from gpdk.components.heater.si_heater import SiHeater
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_si_heater():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += SiHeater(length=50, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    return library
