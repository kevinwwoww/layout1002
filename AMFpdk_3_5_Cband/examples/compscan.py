from fnpcell import all as fp
from AMFpdk import all as pdk
from AMFpdk.technology import get_technology


def comp_scan():
    library = fp.Library()
    TECH = get_technology()

    builder = pdk.CompScanBuilder(
        width=2000,
        spacing=255,
        waveguide_type=TECH.WG.SLAB.C.WIRE,
        fiber_coupler_adapter=pdk.GratingCoupler(waveguide_type=TECH.WG.RIB.C.WIRE),
        bend_factory=TECH.WG.SLAB.C.WIRE.BEND_CIRCULAR
    )
    builder.add_alignment()
    builder.add_title("test", layer=TECH.LAYER.LBL)

    for i in range(10):
        builder.add_block(pdk.RingFilter(ring_radius=20 + i * 10, waveguide_type=TECH.WG.RIB.C.WIRE))

    device = builder.build()
    library += device

    from pathlib import Path
    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name

    fp.export_gds(library, file=gds_file)


if __name__ == "__main__":
    comp_scan()
