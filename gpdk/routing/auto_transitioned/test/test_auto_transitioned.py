from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_auto_transitioned():
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    a1 = pdk.AutoTransitioned(device=pdk.Mmi(waveguide_type=TECH.WG.FWG.C.WIRE), waveguide_types={"*": TECH.WG.FWG.C.WIRE})
    library += a1

    a2 = pdk.AutoTransitioned(device=pdk.Mmi(waveguide_type=TECH.WG.FWG.C.WIRE), waveguide_types={"*": TECH.WG.FWG.C.WIRE})
    assert a1 == a2
    library += a2
    # fmt: on
    # =============================================================
    return library
