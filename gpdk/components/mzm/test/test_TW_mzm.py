from fnpcell import all as fp
from gpdk.components import all as pdk
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True, snap_to_grid=True)
def test_TW_mzm():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += pdk.TW_Mzm(modulator_length=500, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    # fp.plot(library)
    return library
