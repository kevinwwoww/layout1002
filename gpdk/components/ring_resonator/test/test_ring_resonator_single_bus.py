from fnpcell import all as fp
from gpdk.components import all as pdk
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_ring_resonator_single_bus():
    library = fp.Library()

    TECH = get_technology()

    # =======================================================================
    # fmt: off

    library += pdk.RingResonatorSingleBus(ring_type=TECH.WG.FWG.C.WIRE, bottom_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    return library