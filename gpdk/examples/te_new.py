from __future__ import annotations
from fnpcell import all as fp
from fnpcell.all import Point2D, Affine2D
from fnpcell.interfaces import IBendCurveFactory
from fnpcell.geometry.curve_mixin import CurveMixin
import fnpcell.pdk.technology.all as fpt
from functools import cached_property

from dataclasses import dataclass, field, replace
from typing import Tuple, Optional
import numpy as np
import math


# =========================== Generic Curve Definition ===============================
def get_curvature(shape):
    """ calculates the curvature based on the shape """
    x = np.array(shape)[:, 0]
    y = np.array(shape)[:, 1]
    # x = i3.Shape(points=self.shape).points[:, 0]
    # y = i3.Shape(points=self.shape).points[:, 1]
    dx = np.gradient(x)
    ddx = np.gradient(dx)
    dy = np.gradient(y)
    ddy = np.gradient(dy)
    kappa = (dx * ddy - dy * ddx) / (dx ** 2 + dy ** 2) ** (3.0 / 2.0)
    return kappa


@dataclass(eq=False)
class _GenericResolutionCurve(CurveMixin, fp.ICurve):
    resolution: float = field(default=0.5)  # length along the curve. Can be made to find a desired dKappa
    min_bend_radius: float = field(default=20)
    transform: Affine2D = Affine2D.identity()
    start_angle: float = field(default=0, repr=False)
    taper_function: str = field(default="euler", hash=False)
    taper_angle: float = field(default=None)
    taper_length: float = field(default=None)
    p: float = field(default=None)
    origin: Tuple[float, float] = field(default=(0, 0), repr=False)

    @cached_property
    def curve_angles(self) -> Tuple[float, ...]:
        pass

    @property
    def angle_span(self) -> float:

        return self.curve_angles[-1]


    def get_radius_eff(self) -> float:
        points = self.curve_points
        d = abs(fp.distance_between(points[0], points[-1]))
        alpha = abs(0.5 * (np.pi - np.deg2rad(self.angle_span)))
        beta = np.deg2rad(self.angle_span)
        return abs(d * np.sin(alpha) / np.sin(beta))

    @property
    def max_taper_angle(self):
        return 45

    @property
    def radius_eff(self):
        return np.round(self.get_radius_eff(), 3)

    def __post_init__(self):
        if (self.taper_length is None) and (self.taper_angle is None) and (self.p is not None):
            self.taper_angle = self.p * 0.5 * self.angle_span

        if (self.taper_angle is not None) and (self.taper_length is None):
            self.update_taper_length()

        elif (self.taper_length is not None) and (self.taper_angle is None):
            self.update_taper_angle()

        elif (self.taper_length is None) and (self.taper_angle is None) and (self.p is None):
            raise ValueError("Please either set taper_length or taper angle or p")

        else:
            pass

    @property
    def angle_rad(self):
        """
        The final angle (in radians) of the curve.
        """
        return np.deg2rad(self.angle_span)

    def update_taper_angle(self):
        if self.taper_function == "euler":
            taper_length = np.radians(2.0 * self.min_bend_radius * self.taper_angle)

            self.taper_length = abs(taper_length)
            self.p = self.taper_angle / (0.5 * self.angle_span)

    def update_taper_length(self):
        if self.taper_function == "euler":
            taper_length = np.radians(2.0 * self.min_bend_radius * self.taper_angle)

        self.taper_length = abs(taper_length)
        self.p = self.taper_angle / (0.5 * self.angle_span)

    def get_taper_curvature(self):
        no_points_taper = int(abs(self.taper_length) / self.resolution)
        length_res = self.taper_length / (no_points_taper - 1)
        end_curvature = length_res / self.min_bend_radius

        if self.taper_function == "euler":
            curv_range = np.linspace(0.0, np.degrees(end_curvature), no_points_taper)
        return curv_range

    def transform_combined(self: _GenericResolutionCurve, transform: Affine2D) -> _GenericResolutionCurve:
        transform = self.transform @ transform
        return replace(self, transform=transform)

    @property
    def raw_curve_points(self) -> Tuple[Point2D, ...]:
        raise NotImplementedError("Use one of the child classes!")

    @cached_property
    def raw_end_orientations(self) -> Tuple[float, float]:
        """Return the end orientations in math"""
        points = self.raw_curve_points
        o0, o1 = fp.angle_between(points[0], points[1]), fp.angle_between(points[-1], points[-2])
        return np.round(o0, 3), np.round(o1, 3)

    # ==============
    @cached_property
    def curve_points(self) -> Tuple[fp.Point2D, ...]:
        points = self.transform(self.raw_curve_points)
        return self.correct_ends(points, self.end_orientations)  # type: ignore

    @cached_property
    def end_orientations(self) -> Tuple[float, float]:
        """Return orientation of the end"""
        transform = self.transform
        o0, o1 = self.raw_end_orientations
        return fp.normalize_angle(transform.transform_angle(o0)), fp.normalize_angle(transform.transform_angle(o1))

    # print(raw_curve_points[0])


@dataclass(eq=False)
class EulerCurve(_GenericResolutionCurve):
    taper_function: str = field(default="euler", hash=False)
    angle_span: float = field(default=0.0)

    @property
    def max_taper_angle(self):
        return 0.5 * self.angle_span

    @cached_property
    def raw_end_orientations(self) -> Tuple[float, float]:
        """Return the end orientations in math"""
        # here ignores self.start_angle just because I don't know what it is and it defaults to 0
        # start_angle should be considered in this calculation
        return math.radians(180), math.radians(self.angle_span)

    @property
    def raw_curve_points(self) -> Tuple[Point2D, ...]:

        if self.taper_length > 0:
            taper_curvature = self.get_taper_curvature()

            no_points_taper = int(abs(self.taper_length) / self.resolution)
            length_res = self.taper_length / (no_points_taper - 1)
            angles_start = np.cumsum(taper_curvature)

            if angles_start[-1] > self.max_taper_angle:
                raise RuntimeError("The S-bend settings do t allow this routing!")

            angles_stop = (abs(self.angle_span) - angles_start)[::-1]
            n = int((angles_stop[0] - angles_start[-1]) / np.degrees(length_res / self.min_bend_radius))
            angles_middle = np.linspace(
                angles_start[-1] + np.degrees(length_res / self.min_bend_radius), angles_stop[0] - np.degrees(length_res / self.min_bend_radius), n
            )
            angles = np.hstack((angles_start,angles_middle,angles_stop))
            angles = np.insert(angles,0,0)
            angles = np.append(angles,abs(self.angle_span))
        else:
            length_res=self.resolution
            angles = np.arange(
                self.start_angle,
                self.start_angle + abs(self.angle_span) + 0.5 * np.degrees(length_res / self.min_bend_radius),
                np.degrees(length_res / self.min_bend_radius))
            # make sure you are at the correct angle in the beginning and end
            angles = np.insert(angles, 0, 0)
            angles = np.append(angles, abs(self.angle_span))

        # get points:
        coord_x = np.cumsum(length_res * np.cos(np.radians(angles))) + self.origin[0]
        coord_y = np.cumsum(np.sign(np.radians(self.angle_span)) * length_res * np.sin(np.radians(angles))) + self.origin[1]
        # coord_y = np.cumsum(-length_res * np.sin(np.radians(angles))) + self.origin[1] #pdk_base turns downwards

        points_tp = np.vstack((np.hstack((self.origin[0], coord_x)), np.hstack((self.origin[1], coord_y))))
        # then transpose the lot to get an array of coordinates
        points = np.transpose(points_tp)

        # fix the end point onto the grid
        grid = 1e-3  # TECH.METRICS.GRID / TECH.METRICS.UNIT
        points[-1] = (round(points[-1][0] / grid) * grid, round(points[-1][1] / grid) * grid)

        self.curve_angles = angles

        return points.tolist()

            # =========================== Generic Bend Definition ===============================


from gpdk.technology import get_technology

TECH = get_technology()


@dataclass(eq=False)
class _AbstractBendTapering(fp.IWaveguideLike, fp.PCell):
    waveguide_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters", default=TECH.WG.FWG.C.WIRE)

    desired_taper_angle: float = field(default=None)
    desired_taper_length: float = field(default=None)
    min_bend_radius: float = fp.PositiveFloatParam(default=20)
    resolution: float = fp.PositiveFloatParam(default=0.5)  # length along the curve. Can be made to find a desired dKappa
    taper_function: str = fp.TextParam(default="euler", hash=False)
    start_angle: float = fp.FloatParam(default=0, repr=False)
    origin: Tuple[float, float] = fp.ListParam(default=(0, 0), repr=False)
    transform: Affine2D = Affine2D.identity()
    port_names: Sequence[Optional[str]] = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    taper_angle: float = fp.NonNegFloatParam(default=None)
    taper_length: float = fp.NonNegFloatParam(default=None)
    _val_taper = fp.BooleanParam(default=False, doc="boolean to make sure the taper is only validated upon initialization")

    def validate_taper(self):
        self.taper_angle = self.desired_taper_angle
        self.taper_length = self._default_taper_length()

    def __post_init__(self):
        if self.taper_function not in ["euler", "euler_parabolic", "cosine", "standard"]:
            raise ValueError("Please choose euler, euler_parabolic, standard or cosine as taper function.")
        if self._val_taper is False:
        # only evaluate the taper par
            # only evaluate the taper parameters once (upon initialization of the class)
            self.validate_taper()
            self._val_taper = True
        return True

    def _default_taper_angle(self):
        if self.taper_function == "euler":
            angle = np.degrees(self.taper_length / 2.0 / self.min_bend_radius)
        return angle

    def _default_taper_length(self):
        if self.taper_function == "euler":
            taper_length = np.radians(2.0 * self.min_bend_radius * self.taper_angle)
        return taper_length

    def build(self):
        insts, elems, ports = fp.InstanceSet(), fp.ElementSet(), fp.PortSet()

        insts += self.waveguide_type(curve=self.raw_curve).with_ports(self.port_names).with_name(self.name), "wg"

        ports += insts["wg"]["op_0"].with_name("op_0")
        ports += insts["wg"]["op_1"].with_name("op_1")
        return insts, elems, ports

                    # for general implementation, but really not needed at this stage of pdk_base


@dataclass(eq=False)
class EulerBend(_AbstractBendTapering):
    angle_span = fp.DegreeParam(default=90.0)
    p_euler = fp.PositiveFloatParam(default=0.25)
    desired_taper_angle: float = field(default=0)  # this is not used because p_euler takes care of it

    def _default_origin(self):
        return (0, 0)

    @cached_property
    def raw_curve(self):
        curve = EulerCurve(
            resolution=self.resolution,
            min_bend_radius=self.min_bend_radius,
            angle_span=self.angle_span,
            p=self.p_euler,
            transform=self.transform,
            start_angle=self.start_angle,
            taper_function=self.taper_function,
            taper_angle=None,
            taper_length=None,
            origin=self.origin,
        )
        print(curve)
        return curve

                    # =========================== Tapered Bend Factory Definition ===============================


@dataclass(frozen=True)
class TaperedBendFactory(fpt.IBendWaveguideFactory):
    min_bend_radius: float
    waveguide_type: fpt.IWaveguideType = field(repr=False, compare=False)

    def __call__(self, central_angle: float):
        from gpdk.technology.interfaces import CoreCladdingWaveguideType

        degrees_central = math.degrees(central_angle)
        # if abs(degrees_central) > 90:
        #     raise NotImplementedError()

        bend = EulerBend(
            min_bend_radius=self.min_bend_radius, p_euler=0.25,
            waveguide_type=self.waveguide_type, angle_span=abs(degrees_central), resolution=0.01
        )
        if central_angle < 0:
            bend = bend.v_mirrored()
        print(central_angle)

        return bend, bend.raw_curve.radius_eff, ("op_0", "op_1")


# =========================== Routing implementation ===============================
# d = 150
# # points = [(0, 0), (d, 0), (d, d), (10, d), (10, 2 * d)]
# pointts = [(0, 0), (d, 0), (d, d), (10, d), (10, 2 * d)]
#
# route = fp.LinkSmooth(
#     name="link",
#     route=pointts,
#     start_type=TECH.WG.FWG.C.WIRE,
#     end_type=TECH.WG.FWG.C.WIRE,
#     link_type=TECH.WG.FWG.C.WIRE,
#     bend_factory=TaperedBendFactory(min_bend_radius=30.0, waveguide_type=TECH.WG.FWG.C.WIRE),
# )
#
# fp.plot(route)

if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    # library += _AbstractBendTapering()
    library += EulerBend()

    # fmt: on
    # =============================================================
    # fp.export_gds(library, file=gds_file)
    fp.plot(library)

