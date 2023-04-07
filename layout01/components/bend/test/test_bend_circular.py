from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


def test_bend_circular():
    TECH = get_technology()

    fr = 5.0
    sr = 15.0
    short_fwg = pdk.BendCircular(name="s", radius=10, waveguide_type=TECH.WG.FWG.C.WIRE)
    long_fwg = pdk.BendCircular(
        name="d",
        radius=fr * 2,
        waveguide_type=TECH.WG.FWG.C.WIRE,
    ).translated(0, fr * 3)

    transform = fp.translate(0, (fr + sr) * 3)
    short_swg = pdk.BendCircular(name="s", radius=10, waveguide_type=TECH.WG.SWG.C.WIRE, transform=transform)
    long_swg = pdk.BendCircular(
        name="d",
        radius=sr * 2,
        waveguide_type=TECH.WG.SWG.C.WIRE,
        transform=transform,
    ).translated(0, sr * 3)

    cell = fp.Device(name="bend_circular", content=[short_fwg, long_fwg, short_swg, long_swg], ports=[])

    return cell
