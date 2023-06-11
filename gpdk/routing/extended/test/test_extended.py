from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_extended():
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off
    from gpdk.components.mmi.mmi import Mmi

    e1 = pdk.Extended(device=Mmi(waveguide_type=TECH.WG.FWG.C.WIRE), lengths={"*": 10, "op_0": 20, "op_1": 30})
    library += e1

    e2 = pdk.Extended(device=Mmi(waveguide_type=TECH.WG.FWG.C.WIRE), lengths={"*": 10, "op_0": 20, "op_1": 30})
    assert e1 == e2
    # fmt: on
    # =============================================================
    return library
