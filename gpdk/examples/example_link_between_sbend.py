from random import randint
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology

if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================

    distance = 400
    height = 100
    ec = pdk.Fixed_Edge_Coupler()
    pd = pdk.Fixed_Photo_Detector().translated(distance, height)

    x = 0
    y = 0
    n = 10
    d = distance / (n + 3)
    waypoints: fp.IWaypoints = []
    while n > 0:
        x += d
        y += randint(1, 40) / 8
        waypoints.append(fp.Waypoint(x, y, 0))
        n -= 1

    wg = fp.LinkBetween(
        start=ec["op_0"],
        end=pd["op_0"],
        link_type=TECH.WG.FWG.C.WIRE,
        # bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
        waypoints=waypoints,
    )
    library += wg
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
