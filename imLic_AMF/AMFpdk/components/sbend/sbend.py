import math
from dataclasses import dataclass
from typing import List, Optional, Tuple, cast
from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt
from AMFpdk.technology import get_technology
from AMFpdk.util import all as util
from AMFpdk.components.straight.straight import StraightBetween

@dataclass(eq=False)
class SBend(fp.PCell):
    distance: Optional[float] = fp.PositiveFloatParam(required=False)
    height: float = fp.FloatParam(default=10, invalid=[0])
    bend_degrees: Optional[float] = fp.DegreeParam(required=False)
    max_distance: float = fp.PositiveFloatParam(required=False)
    bend_factory: fp.IBendWaveguideFactory = fp.Param(required=False)
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=("op_0", "op_1"))

    def _default_bend_degrees(self):
        if self.distance is None:
            return 45

    def _default_waveguide_type(self):
        return get_technology().WG.RIB.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        distance = self.distance
        height = self.height
        bend_degrees = self.bend_degrees
        max_distance = self.max_distance
        bend_factory = self.bend_factory
        waveguide_type = self.waveguide_type
        port_names = self.port_names


        assert distance or bend_degrees is not None, "either distance or bend_degrees must be supplied"
        if bend_factory is None:
            bend_factory = waveguide_type.bend_factory

        reflect = height < 0
        height = abs(height)
        bend = None
        port_in = "op_0"
        port_out = "op_1"

        if distance is None:
            assert bend_degrees is not None
            central_angle = math.radians(bend_degrees)
            assert 0 < central_angle < math.pi
            bend, _, (port_in, port_out) = bend_factory(central_angle)
            bend = fp.place(bend, port_in, at=fp.Waypoint(0, 0, 0))
            ex, ey = bend[port_out].position
            distance = (height - ey * 2) / math.tan(central_angle) + ex * 2

        if max_distance is not None and distance > max_distance:
            distance = max_distance
            bend = None

        if bend is None:
            central_angle = _get_central_angle(distance=distance, height=height, bend_factory=bend_factory)
            bend, _, (port_in, port_out) = bend_factory(central_angle)
            bend = fp.place(bend, port_in, at=fp.Waypoint(0, 0, 0))

        assert bend is not None

        bend = bend.translated(-distance / 2, -height / 2)

        start_bend = bend
        end_bend = bend.c_mirrored()

        if reflect:
            start_bend = start_bend.v_mirrored()
            end_bend = end_bend.v_mirrored()

        insts += start_bend
        ports += start_bend[port_in].with_name(port_names[0])

        insts += end_bend
        ports += end_bend[port_in].with_name(port_names[1])

        if cast(fp.IPort, bend[port_out]).waveguide_type != waveguide_type:
            buffer:List[fp.ICelllRef] = []
            t1 = util.links.transition_start(TECH, buffer, start=cast(fp.IPort, start_bend[port_out]), final_type=waveguide_type)
            insts += buffer[0]
            buffer = []
            t2 = util.links.transition_start(TECH, buffer, start=cast(fp.IPort, end_bend[port_out]), final_type=waveguide_type)
            insts += buffer[0]
            straight = StraightBetween(start=t1.position, end=t2.position, waveguide_type=waveguide_type)
        else:
            straight = StraightBetween(start=start_bend[port_out].position, end=end_bend[port_out].position, waveguide_type=waveguide_type)

        insts += straight

        return insts, elems, ports

def _get_central_angle(*, distance: float, height: float, bend_factory: fp.IBendWaveguideFactory):
    epsilon = fpt.grid_unit() / 20 / fpt.user_unit()
    d = distance / 2
    h = height / 2
    ls = (h**2 + d**2) / (2 * d)
    if height == distance:
        max_angle = math.pi / 2.0
    else:
        max_angle = math.atan(h / (d - ls))
    central_angle = max_angle
    while True:
        bend, radius_eff, (_, port_out) = bend_factory(central_angle)
        ex, ey = bend[port_out].position
        line_angle = math.atan2(h - ey, d - ex)
        assert line_angle > 0, "radius_min too large"

        if fp.is_close(radius_eff * line_angle, radius_eff * central_angle, epsilon=epsilon):
            return central_angle

        central_angle = (central_angle + line_angle) / 2

def SBendPair(
        *,
        left_spacing: float,
        right_spacing: float,
        top_type: fp.IWaveguideType,
        bottom_type: fp.IWaveguideType,
        top_distance: Optional[float] = None,
        bottom_distance: Optional[float] = None,
        bend_degrees: Optional[float] = None,
        top_bend_factory: Optional[fp.IBendWaveguideFactory] = None,
        bottom_bend_factory: Optional[fp.IBendWaveguideFactory] = None,
):
    assert top_distance or bend_degrees
    assert bottom_distance or bend_degrees
    sbend_height = (left_spacing - right_spacing) / 2
    dy = sbend_height / 2 + right_spacing / 2

    top = SBend(
        name="top",
        distance=top_distance,
        bend_degrees=bend_degrees,
        height=-sbend_height,
        bend_factory=top_bend_factory or top_type.bend_factory,
        waveguide_type=top_type,
        transform=fp.translate(0, dy),
    )
    bottom = SBend(
        name="bottom",
        distance=top_distance,
        bend_degrees=bend_degrees,
        height=sbend_height,
        bend_factory=bottom_bend_factory or bottom_type.bend_factory,
        waveguide_type=bottom_type,
        transform=fp.translate(0, -dy),
    )

    return top, bottom

if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file
    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    # from AMFpdk import all as pdk

    library += SBend()

    fp.export_gds(library, file=gds_file)