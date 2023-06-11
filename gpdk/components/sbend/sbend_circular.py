import math
from dataclasses import dataclass
from typing import Optional, Tuple, cast

from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class SBendCircular(fp.PCell):
    """
    Attributes:
        distance: defaults to 20
        height: defaults to 10
        min_radius: required=False
        waveguide_type: type of waveguide
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
        sbend = SBendCircular(name="f", distance=100, height=15, min_radius=15, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(sbend)
    ```
    ![SBendCircular](images/sbend_circular.png)
    """

    distance: float = fp.PositiveFloatParam(default=20)
    height: float = fp.FloatParam(default=10, invalid=[0])
    min_radius: Optional[float] = fp.PositiveFloatParam(required=False)
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=("op_0", "op_1"))

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        # fmt: off

        distance = self.distance
        height = self.height
        min_radius =self.min_radius
        waveguide_type = self.waveguide_type
        port_names = self.port_names
        min_radius_of_type = cast(float, waveguide_type.BEND_CIRCULAR.radius_eff)  # type: ignore
        if min_radius is None:
            min_radius = min_radius_of_type
        reflect = height < 0
        height = abs(height)
        cx, cy = distance / 2, height / 2
        r = (cx ** 2 + cy ** 2) / height
        assert fp.is_close(r, min_radius) or (r >= min_radius >= min_radius_of_type), "sbend_circular: min_radius must be greater than min_radius_of_type"
        theta = math.acos((r - cy) / r)

        elliptical_arc = fp.g.EllipticalArc(
            radius=r,
            initial_degrees=-90,
            final_radians=-math.pi / 2 + theta,
            origin=(-cx, r - cy),
        )
        path = (
            fp.g.Path.move(to=(-cx, -cy))
            .appended(elliptical_arc)
            .appended(elliptical_arc.c_mirrored(), reverse=True, end_at=(cx, cy))
        )
        if reflect:
            path = path.v_mirrored()

        # fmt: on
        wg = waveguide_type(path).with_ports(port_names)
        insts += wg
        ports += wg.ports
        return insts, elems, ports


def _get_sbend_distance(*, height: float, bend_degrees: float, min_radius: float) -> float:
    h = height / 2
    bend_angle = math.radians(bend_degrees)
    bend_radius = max(h / (1 - math.cos(bend_angle)), min_radius)
    d = bend_radius * math.sin(bend_angle)
    return fp.snap_ceil(max(d * 2, height))


@dataclass(eq=False)
class SBendCircularPair(fp.PCell):
    left_spacing: float = fp.PositiveFloatParam()
    right_spacing: float = fp.PositiveFloatParam()
    bend_degrees: float = fp.DegreeParam()
    min_radius: Optional[float] = fp.PositiveFloatParam(required=False)
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4, default=("op_0", "op_1", "op_2", "op_3"))

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        # fmt: off

        left_spacing = self.left_spacing
        right_spacing = self.right_spacing
        bend_degrees = self.bend_degrees
        min_radius = self.min_radius
        waveguide_type = self.waveguide_type
        port_names = self.port_names
        if min_radius is None:
            min_radius = cast(float, waveguide_type.BEND_CIRCULAR.radius_eff)  # type: ignore

        total_height = left_spacing - right_spacing
        sbend_height = total_height / 2
        if sbend_height > 0:
            dy = sbend_height / 2 + right_spacing / 2
            transform0, transform1 = fp.v_mirror().translate(0, dy), fp.translate(0, -dy)
        else:  # sbend_height < 0:
            sbend_height = -sbend_height
            dy = sbend_height / 2 + left_spacing / 2
            transform0, transform1 = fp.translate(0, dy), fp.v_mirror().translate(0, -dy)
        sbend_distance = _get_sbend_distance(height=sbend_height, bend_degrees=bend_degrees, min_radius=min_radius)

        sbend_0 = SBendCircular(name="0", distance=sbend_distance, height=sbend_height, min_radius=min_radius, waveguide_type=waveguide_type, transform=transform0)
        sbend_1 = SBendCircular(name="1", distance=sbend_distance, height=sbend_height, min_radius=min_radius, waveguide_type=waveguide_type, transform=transform1)

        insts += sbend_0
        insts += sbend_1
        ports += sbend_0["op_0"].with_name(port_names[0])
        ports += sbend_0["op_1"].with_name(port_names[3])
        ports += sbend_1["op_0"].with_name(port_names[1])
        ports += sbend_1["op_1"].with_name(port_names[2])

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += SBendCircular()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
