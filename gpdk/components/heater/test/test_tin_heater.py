from fnpcell import all as fp
from gpdk.components.heater.tin_heater import TiNHeater
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_tin_heater():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += TiNHeater(waveguide_length=50, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    return library
