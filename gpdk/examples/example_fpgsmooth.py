from fnpcell import all as fp
from gpdk.technology import get_technology


TECH = get_technology()

def bend_factory(central_angle: float):
    bend = fp.g.CircularBend(radius=20, radians=central_angle)
    return bend, 20


waypoints = [(10, 0), (10, 100), (100, 100), (100, 200)]
curve = fp.g.Path.smooth(waypoints=waypoints, bend_factory=bend_factory)
wg1 = TECH.WG.FWG.C.WIRE(curve=curve)
fp.plot(wg1)
