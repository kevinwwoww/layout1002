import math
from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(frozen=True)
class Cosine(fp.g.FunctionCurve):
    radius_eff: Optional[float] = None
    radius_min: Optional[float] = None
    degrees: Optional[float] = None
    radians: Optional[float] = None
    p: Optional[float] = None
    l_max: Optional[float] = None
    transform: fp.Affine2D = fp.Affine2D.identity()
    """
    :param degrees
        central angle in degrees

    :param radius_min radius minimum
    :param radius_eff radius effective
        choose either radius_min(imum) or radius_eff(ective)

    :param p radio of euler spiral in whole bend, 0 < p <= 1, when p = 1, there's no cirular part in the bend
    :param l_max max length of euler spiral in half bend
        choose either p or l_max

    """

    def __post_init__(self):
        assert self.radians or self.degrees, "either radians or degrees must be a non-zero value"
        assert self.radius_eff or self.radius_min, "either radius_eff or radius_min must be a non-zero value"
        assert self.p is None or 0 <= self.p <= 1, "bend paramter p must be in [0, 1]"
        assert self.radius_eff or (self.radius_min and self.p != 1), " if radius_min is not None, p must not 1"

    @staticmethod
    def p_from_l_max(l_max: float, radius_min: float, central_angle: float) -> float:
        return min(1, abs(l_max / radius_min / central_angle))

    def curve_function(self, t: float):

        if self.degrees is None:
            central_angle = math.pi / 2
        else:
            central_angle = math.radians(self.degrees)
        central_angle = fp.normalize_angle(central_angle)

        if self.p is not None:
            p = 1 - self.p
        else:
            if self.l_max and self.radius_min:
                p = self.p_from_l_max(l_max=self.l_max, radius_min=self.radius_min, central_angle=central_angle)
            else:
                p = 1

        t = fp.clamp(t, 0, 1)

        # f(x)=c*sin(a*x) f(x)'=ac*cos(a*x)
        k0 = math.tan(central_angle / 2)
        k1 = math.tan(p * central_angle / 2)
        if self.radius_eff is None and self.radius_min is not None:
            t0 = self.radius_min * (2 * math.sin(p * central_angle / 2))
            t1 = math.acos(k1 / k0)
            a = (math.pi - 2 * t1) / t0
            r = math.pi * (math.sqrt(k0 * k0 + 1)) / (2 * a * k0)
        else:
            r = self.radius_eff
            assert r
            a = math.pi * (math.sqrt(k0 * k0 + 1)) / (2 * r * k0)
        c = k0 / a

        x0 = math.acos(k1 / k0) / a
        y0 = c * math.sin(a * x0)
        theta = math.pi / a
        x1 = x0 / theta
        if p == 0:
            r_min = 0
        elif self.radius_min is None:
            r_min = (theta - 2 * x0) / (2 * math.sin(p * central_angle / 2))
        else:
            # r_min_1 = (theta - 2 * x0) / (2 * math.sin(p * central_angle / 2))
            r_min = self.radius_min

        dx = math.sin(p * central_angle / 2) * r_min
        c_a = x0 + dx
        c_b = y0 - math.sqrt(abs(r_min**2 - dx**2))

        if t <= x1:
            x = theta * t
            y = c * math.sin(a * x)
        elif x1 < t < (x1 + 2 * dx / theta):
            x = theta * t
            y = math.sqrt(r_min**2 - (x - c_a) ** 2) + c_b
        else:
            x = theta * t
            y = c * math.sin(a * x)

        return x, y


@dataclass(eq=False)
class BendCosine(fp.IWaveguideLike, fp.PCell):
    radius_eff: float = fp.PositiveFloatParam(required=False)
    degrees: float = fp.DegreeParam(default=90, min=-90, max=90)
    radius_min: float = fp.PositiveFloatParam(required=False, doc="Bend radius_min")
    p: float = fp.FloatParam(default=0.5, max=1, doc="Bend parameter")
    l_max: float = fp.PositiveFloatParam(default=math.inf, doc="Bend Lmax")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    @cached_property
    def raw_curve(self):
        return Cosine(radius_eff=self.radius_eff, radius_min=self.radius_min, degrees=self.degrees, p=self.p, l_max=self.l_max)

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

    library += BendCosine(radius_min=50, degrees=90, p=0.5, waveguide_type=TECH.WG.FWG.C.WIRE)
    library += BendCosine(radius_min=50, degrees=90, p=0, waveguide_type=TECH.WG.FWG.C.WIRE)
    library += BendCosine(radius_eff=100, degrees=90, p=0.5, waveguide_type=TECH.WG.FWG.C.WIRE).translated(0, 100)
    library += BendCosine(radius_eff=100, degrees=90, p=1, waveguide_type=TECH.WG.FWG.C.WIRE).translated(0, 100)
    # library += BendCosine(radius_eff=100, degrees=90, p=0.5, waveguide_type=TECH.WG.FWG.C.WIRE)
    # library += BendCosine(radius_eff=100, degrees=90, p=1, waveguide_type=TECH.WG.FWG.C.WIRE)
    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
