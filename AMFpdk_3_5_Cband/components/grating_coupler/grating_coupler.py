from dataclasses import dataclass
import math
from typing import List, Tuple, cast
from fnpcell import all as fp

from AMFpdk.technology import get_technology
from AMFpdk.technology.interfaces import CoreWaveguideType


@dataclass(eq=False)
class GratingCoupler(fp.PCell):
    length: float = fp.PositiveFloatParam(default=25.0)
    half_degrees: float = fp.DegreeParam(default=20)
    ellipse_ratio: float = fp.PositiveFloatParam(default=1.0, min=1.0, doc="Ellipse(Major/Minor")
    tooth_width: float = fp.PositiveFloatParam(default=0.5)
    etch_width: float = fp.PositiveFloatParam(default=0.5)
    teeth: int = fp.IntParam(default=30, min=0, doc="Number of tooth")
    waveguide_type: CoreWaveguideType = fp.WaveguideTypeParam(type=CoreWaveguideType)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=1, default=["op_0"])

    def _default_waveguide_type(self):
        return get_technology().WG.RIB.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        length = self.length
        half_degrees = self.half_degrees
        ellipse_ratio = self.ellipse_ratio
        tooth_width = self.tooth_width
        etch_width = self.etch_width
        teeth = self.teeth
        waveguide_type = self.waveguide_type
        port_names = self.port_names

        overlap = 1.0
        fiber_pin_width = 5

        half_angle = math.radians(half_degrees)
        waveguide_width = waveguide_type.wg_width
        waveguide_layer = waveguide_type.wg_layer
        si_etch1_layer = TECH.WG.GRAT.C.WIRE.wg_layer

        content:List[fp.IPolygon] = []
        content.append(
            fp.el.EllipticalRing(outer_radius=(length, length / ellipse_ratio), layer=waveguide_layer,
                                 transform=fp.h_mirror())
        )

        final_tooth_radius = length
        for _ in range(teeth):
            final_tooth_radius = final_tooth_radius + etch_width

            inner_radius_x = final_tooth_radius
            inner_radius_y = inner_radius_x / ellipse_ratio

            final_tooth_radius = final_tooth_radius + tooth_width

            outer_radius_x = final_tooth_radius
            outer_radius_y = outer_radius_x / ellipse_ratio

            content.append(fp.el.EllipticalRing(outer_radius=(outer_radius_x, outer_radius_y),
                                                inner_radius=(inner_radius_x, inner_radius_y), layer=waveguide_layer,
                                                transform=fp.h_mirror()))

        delta_radius = (waveguide_width / 2.0) / math.tan(half_angle)
        wedge_y = math.tan(half_angle) * (delta_radius + final_tooth_radius)

        trapezoid = fp.el.Line(length=final_tooth_radius, stroke_width=waveguide_width, final_stroke_width=wedge_y * 2,
                               layer=waveguide_layer)

        content = list(fp.el.PolygonSet(content, layer=waveguide_layer) & trapezoid)

        fiber_pin_tooth = 1 + int(teeth / 2)
        fiber_pin_x = min(content[fiber_pin_tooth].polygon_points, key=lambda p: p[0])[0]

        overlap_x = final_tooth_radius + overlap
        overlap_y = overlap_x / ellipse_ratio

        overlap_polygon = fp.el.EllipticalRing(outer_radius=(overlap_x, overlap_y), layer=si_etch1_layer, transform=fp.rotate(radians=math.pi))

        inner_angle = math.pi / 2 - half_angle
        perpendicular_overlap = overlap / math.sin(inner_angle)
        overlap_delta = (perpendicular_overlap + (waveguide_width / 2)) / math.tan(half_angle)
        overlap_wedge_y = math.tan(half_angle) * (overlap_delta + final_tooth_radius + overlap)
        trapezoid = fp.el.Line(length=overlap_x, stroke_width=waveguide_width + perpendicular_overlap * 2, final_stroke_width=overlap_wedge_y * 2, layer=si_etch1_layer)
        overlap_polygon &= trapezoid

        elements = cast(List[fp.IElement], content)
        elements.extend(
            [
                fp.el.Line(length=fiber_pin_width, stroke_width=fiber_pin_width, layer=get_technology().LAYER.LBL,
                           transform=fp.translate(fiber_pin_x, 0)),
                fp.el.Text(content="optFiber", text_anchor=fp.Anchor.CENTER, vertical_align=fp.VertialAlign.MIDDLE,
                           layer=get_technology().LAYER.LBL, at=(fiber_pin_x + fiber_pin_width / 2, 0)),
            ]
        )
        ports += fp.Port(name=port_names[0], position=(0, 0), orientation=math.pi, waveguide_type=waveguide_type)

        elems += elements

        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += GratingCoupler()

    fp.export_gds(library, file=gds_file)
