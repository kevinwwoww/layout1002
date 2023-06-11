from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.technology.waveguide_factory import CircularBendFactory


def comp_scan():
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    builder = pdk.CompScanBuilder(
        width=2000,
        spacing=255,
        waveguide_type=TECH.WG.SWG.C.EXPANDED,
        fiber_coupler_adapter=pdk.GratingCoupler(waveguide_type=TECH.WG.FWG.C.WIRE))
    builder.add_alignment()
    builder.add_title("Circuit04", layer=TECH.LAYER.LABEL_DRW)
    bend_factory = CircularBendFactory(radius_eff=100, waveguide_type=TECH.WG.FWG.C.WIRE)
    for i in range(5):
        builder.add_block(pdk.RingFilter(ring_radius=10 + i * 5, waveguide_type=TECH.WG.FWG.C.WIRE), bend_factory=bend_factory)


    device = builder.build()
    library += device

    # fmt: on
    # =============================================================
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name

    fp.export_gds(library, file=gds_file)


if __name__ == "__main__":
    comp_scan()
