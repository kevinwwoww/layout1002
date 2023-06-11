import math
import numpy as np
from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from fnpcell import all as fp
from fnpcell.geometry.curve_mixin import CurveMixin
from gpdk.technology import get_technology


@fp.hash_code
@dataclass(frozen=True)
class EllipticalArc(CurveMixin, fp.IUpdatable, fp.ICurve):
    radius: Tuple[float, float]
    initial_angle: float
    final_angle: float
    transform: fp.Affine2D

    #########################################################
    @cached_property
    def raw_curve_points(self) -> Tuple[fp.Point2D, ...]:
        step = math.radians(1)
        initial_angle = self.initial_angle
        final_angle = self.final_angle
        radius_x, radius_y = self.radius
        n = int(math.ceil(abs(final_angle - initial_angle) / step + 0.5))
        angles = np.linspace(initial_angle, final_angle, n)  # type: ignore
        xs = radius_x * np.cos(angles)  # type: ignore
        ys = radius_y * np.sin(angles)  # type: ignore

        points_tp = np.vstack((xs, ys))  # type: ignore
        points = np.transpose(points_tp)  # type: ignore
        return points  # type: ignore

    @cached_property
    def raw_end_orientations(self) -> Tuple[float, float]:
        """Return the end orientations in math"""
        points = self.raw_curve_points
        o0, o1 = fp.angle_between(points[0], points[1]), fp.angle_between(points[-1], points[-2])

        return o0, o1

    ##########################################################

    def transform_combined(self, transform: fp.Affine2D) -> "EllipticalArc":
        transform = self.transform @ transform
        return self.updated(transform=transform)

    ##########################################################

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


@dataclass(eq=False)
class CustomWaveguide(fp.IWaveguideLike, fp.PCell):
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    @cached_property
    def raw_curve(self):
        return EllipticalArc(radius=(20, 10), initial_angle=0, final_angle=math.radians(30), transform=fp.Affine2D.identity())

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

    library += CustomWaveguide(waveguide_type=TECH.WG.FWG.C.WIRE).rotated(degrees=90).translated(200, 0)
    library += CustomWaveguide(waveguide_type=TECH.WG.FWG.C.WIRE).rotated(degrees=90).translated(-200, 0)
    library += CustomWaveguide(waveguide_type=TECH.WG.FWG.C.WIRE).translated(0, 100)
    library += CustomWaveguide(waveguide_type=TECH.WG.FWG.C.WIRE).translated(0, 100)
    # library += BendCosine(radius_eff=100, degrees=90, p=0.5, waveguide_type=TECH.WG.FWG.C.WIRE)
    # library += BendCosine(radius_eff=100, degrees=90, p=1, waveguide_type=TECH.WG.FWG.C.WIRE)
    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
