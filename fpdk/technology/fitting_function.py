from dataclasses import dataclass
from typing import Iterable

from fnpcell import all as fp


class FITTING_FUNCTION:
    @dataclass(frozen=True)
    class Stubbed:
        stub_width: float
        stub_right_angle: bool

        def __call__(self, waypoints: Iterable[fp.Point2D]) -> fp.ICurve:
            return fp.g.Path.stubbed(waypoints=waypoints, stub_width=self.stub_width, stub_right_angle=self.stub_right_angle)

    @dataclass(frozen=True)
    class SmoothCircular:
        radius: float

        def bend_factory(self, central_angle: float):
            bend = fp.g.CircularBend(radius=self.radius, radians=central_angle)
            return bend, self.radius

        def __call__(self, waypoints: Iterable[fp.Point2D]) -> fp.ICurve:
            return fp.g.Path.smooth(waypoints=waypoints, bend_factory=self.bend_factory)
