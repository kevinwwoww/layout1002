import math
from dataclasses import dataclass
from functools import cached_property
from typing import List, Tuple

from fnpcell import all as fp
from gpdk.components.bend.bend_euler import BendEuler90
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class Spiral(fp.PCell):
    """
    Attributes:
        bend_radius: defaults to 5
        min_straight: defaults to 0
        spacing: defaults to 6
        total_length: defaults to 4000.0
        n_o_loops: defaults to 5
        waveguide_type: type of waveguide
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
        spiral = Spiral(total_length=2000, n_o_loops=6, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(spiral)
    ```
    ![Spiral](images/spiral.png)
    """

    bend_radius: float = fp.PositiveFloatParam(default=5)
    min_straight: float = fp.FloatParam(default=0)
    spacing: float = fp.PositiveFloatParam(default=6)
    total_length: float = fp.PositiveFloatParam(default=4000.0)
    n_o_loops: int = fp.IntParam(default=5)
    waveguide_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _get_spiral_inner_polyline(self):
        r = self.bend_radius
        ms = self.min_straight
        sp = self.spacing
        points = [
            (0, -2 * sp),
            (0, 3 * r + 2 * ms - sp),
            (-2 * r - sp, 3 * r + 2 * ms - sp),
            (-2 * r - sp, r + ms - sp),
            (-sp, r + ms - sp),
            (-sp, -r - sp),
            (-2 * r - 2 * sp, -r - sp),
            (-2 * r - 2 * sp, 3 * r + 2 * ms),
            (sp, 3 * r + 2 * ms),
            (sp, -3 * sp),
        ]

        return fp.g.Polyline(points[::-1])

    def _get_spiral_loop_polyline(self, ver_loop: float, hor_loop: float):
        r = self.bend_radius
        sp = self.spacing

        points = [
            (0, 0),
            (0, ver_loop + r),
            (-2 * r - hor_loop - 2 * sp, ver_loop + r),
            (-2 * r - hor_loop - 2 * sp, -r + 2 * sp),
            (-2 * sp, -r + 2 * sp),
            (-2 * sp, 2 * sp),
        ]

        return fp.g.Polyline(points)

    def _get_spiral_end_polyline(self):
        r = self.bend_radius

        points = [
            (0, 0),
            (0, -r),
            (-r, -r),
        ]

        return fp.g.Polyline(points)

    @cached_property
    def bend90(self):
        return BendEuler90(
            radius_eff=self.bend_radius,
            slab_square=False,
            waveguide_type=self.waveguide_type,
        )

    def bend_factory(self, central_angle: float):
        if not fp.is_close(abs(central_angle), math.pi / 2):
            raise NotImplementedError()
        bend = self.bend90
        result = bend if central_angle > 0 else bend.v_mirrored()
        return result, bend.raw_curve.radius_eff, ("op_0", "op_1")

    def route(self):
        n_o_loops = self.n_o_loops
        left_routes: List[fp.ICurve] = []
        right_routes: List[fp.ICurve] = []

        inner_polyline = self._get_spiral_inner_polyline()
        ray_in, ray_out = inner_polyline.end_rays
        # right_routes.append(inner_polyline)

        n_o_loops -= 1
        for i in range(0, n_o_loops):
            hor_loop = 2 * i * self.spacing + 3 * self.spacing
            ver_loop = 2 * self.bend_radius + 2 * self.min_straight + 2 * i * self.spacing + 5 * self.spacing

            polyline = self._get_spiral_loop_polyline(hor_loop=hor_loop, ver_loop=ver_loop)

            if i % 2 == 0:
                transform = fp.transform_between(polyline.end_rays[1], ray_out)
                polyline = fp.g.Polyline(reversed(polyline.curve_points))
                polyline = polyline.transform_combined(transform)
                right_routes.append(polyline)
                ray_out = polyline.end_rays[1]
            else:
                transform = fp.transform_between(polyline.end_rays[1], ray_in)
                polyline = polyline.transform_combined(transform)
                left_routes.insert(0, polyline)
                ray_in = polyline.end_rays[0]

        final_polyline = self._get_spiral_end_polyline()

        if n_o_loops % 2 == 0:
            final_polyline = final_polyline.h_mirrored()
        transform = fp.transform_between(final_polyline.end_rays[1], ray_out)
        end_polyline = fp.g.Polyline(reversed(final_polyline.curve_points))
        end_polyline = end_polyline.transform_combined(transform)
        right_routes.append(end_polyline)

        start_polyline = final_polyline.h_mirrored()
        transform = fp.transform_between(start_polyline.end_rays[1], ray_in)
        start_polyline = start_polyline.transform_combined(transform)
        left_routes.insert(0, start_polyline)

        left_waypoints: List[fp.Point2D] = []
        for it in left_routes:
            curve_points = it.curve_points
            if left_waypoints and left_waypoints[-1] == curve_points[0]:
                left_waypoints.pop()
            left_waypoints.extend(curve_points)

        right_waypoints: List[fp.Point2D] = []
        for it in right_routes:
            curve_points = it.curve_points
            if right_waypoints and right_waypoints[-1] == curve_points[0]:
                right_waypoints.pop()
            right_waypoints.extend(curve_points)

        center_link = fp.LinkSmooth(
            inner_polyline.curve_points,
            link_type=self.waveguide_type,
            bend_factory=self.bend_factory,
        )
        left_link = fp.LinkSmooth(left_waypoints, link_type=self.waveguide_type, bend_factory=self.bend_factory)
        right_link = fp.LinkSmooth(right_waypoints, link_type=self.waveguide_type, bend_factory=self.bend_factory)
        left_n = int(n_o_loops / 2) * 6
        right_n = int((n_o_loops + 1) / 2) * 6
        delta_length = self.total_length - center_link.curve_length
        delta_unit = delta_length / (left_n + right_n)

        return (
            fp.LinkSmooth(
                left_waypoints,
                link_type=self.waveguide_type,
                bend_factory=self.bend_factory,
                target_length=left_link.curve_length + delta_unit * left_n,
            ),
            center_link,
            fp.LinkSmooth(
                right_waypoints,
                link_type=self.waveguide_type,
                bend_factory=self.bend_factory,
                target_length=right_link.curve_length + delta_unit * right_n,
            ),
        )

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        left, center, right = self.route()

        insts += left, center, right
        ports += []

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += Spiral(total_length=2000, n_o_loops=5, waveguide_type=TECH.WG.FWG.C.WIRE)
    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
