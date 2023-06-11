from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_comp_scan():
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================

    builder = pdk.CompScanBuilder(
        width=2000, spacing=255, waveguide_type=TECH.WG.SWG.C.WIRE, fiber_coupler_adapter=pdk.GratingCoupler(waveguide_type=TECH.WG.FWG.C.WIRE)
    )
    builder.add_alignment()
    builder.add_title("CIRCUIT04", layer=TECH.LAYER.LABEL_DRW)
    for i in range(10):
        builder.add_block(pdk.RingFilter(ring_radius=10 + i * 5, waveguide_type=TECH.WG.FWG.C.WIRE))

    device = builder.build()
    library += device

    return library


if __name__ == "__main__":
    test_comp_scan()
