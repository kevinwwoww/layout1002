from typing import Optional, Tuple

from fnpcell import all as fp


class TPoint2D(Tuple[float, float]):
    def __new__(cls, x: float, y: float):
        return tuple.__new__(TPoint2D, (x, y))  # type: ignore

    def translated(self, tx: float, ty: float):
        return TPoint2D(*fp.translate(tx, ty).transform_point(self))

    def rotated(
        self,
        *,
        degrees: Optional[float] = None,
        radians: Optional[float] = None,
        origin: fp.Point2D = (0, 0),
    ):
        return TPoint2D(*fp.rotate(degrees=degrees, radians=radians, center=origin).transform_point(self))

    def h_mirrored(self, *, x: float = 0):
        """Horizontal mirrored"""
        return TPoint2D(*fp.h_mirror(x=x).transform_point(self))

    def v_mirrored(self, *, y: float = 0):
        """Vertical mirrored."""
        return TPoint2D(*fp.v_mirror(y=y).transform_point(self))

    def c_mirrored(self, *, center: fp.Point2D = (0, 0)):
        """Center mirrored."""
        return TPoint2D(*fp.c_mirror(center=center).transform_point(self))


if __name__ == "__main__":

    from gpdk.technology import get_technology

    p = TPoint2D(0, 0)
    points = [p, p.translated(100, 0), p.translated(100, 0).rotated(degrees=30)]
    polyline = fp.el.Polyline(points, layer=get_technology().LAYER.FLYLINE_MARK).rotated(degrees=15)
    fp.plot(polyline)
