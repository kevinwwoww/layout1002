from dataclasses import dataclass
from functools import cached_property
from typing import Sequence, Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class BendBezier(fp.IWaveguideLike, fp.PCell):
    """
    Attributes:
        start: start point of bezier curve
        controls: control points of bezier, 1 for Quadratic Bezier, 2 for Cubic Bezier, ...
        end: end point of bezier curve
        waveguide_type: type of waveguide of the bend
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
        bend = BendBezier(name="q", start=(0, 0), controls=[(31, 30)], end=(60, 0), waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(bend)
    ```
    ![BendBezier](images/bend_bezier_q.png)
    """

    start: fp.Point2D = fp.PositionParam(default=(0, 0), doc="position where bend start, eg. (x, y)")
    controls: Sequence[fp.Point2D] = fp.PointsParam(default=[(10, 0)], min_count=1, doc="control points, count >= 1, eg. [(x1, y1), (x2, y2)]")
    end: fp.Point2D = fp.PositionParam(default=(10, 10), doc="position where bend end, eg. (x, y)")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    @cached_property
    def raw_curve(self):
        return fp.g.Bezier(
            start=self.start,
            controls=self.controls,
            end=self.end,
        )

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        wg = self.waveguide_type(curve=self.raw_curve).with_ports(self.port_names)
        insts += wg
        ports += wg.ports
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += BendBezier()
    # library += BendBezier(name="q", start=(0, 0), controls=[(31, 30)], end=(60, 0), waveguide_type=TECH.WG.FWG.C.WIRE)
    # library += BendBezier(name="c", start=(0, 0), controls=[(0, 30), (60, 30)], end=(60, 0), waveguide_type=TECH.WG.FWG.C.WIRE, transform=fp.translate(0, 40))

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
