from dataclasses import dataclass
from typing import  Tuple, List, cast
from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt

from SITRI_pdk.technology.interfaces import CrackedMetalLineType
from SITRI_pdk.technology.metal import METAL

@dataclass(frozen=True)
class _Vias(fpt.IViasFactory):
    initial_type: CrackedMetalLineType
    final_type: CrackedMetalLineType
    top_layer: fpt.ILayer
    via_layer: fpt.ILayer
    bottom_layer: fpt.ILayer

    def __call__(self, curve: fpt.ICurve, length: float) -> Tuple[fpt.IElement, Tuple[float,float]]:
        from SITRI_pdk.components.via.via import Via
        from SITRI_pdk.components.via.vias import Vias
        from SITRI_pdk.technology import get_technology

        TECH = get_technology()
        spacing = TECH.VIAS.SPACING
        overlap = TECH.VIAS.OVERLAP
        initial_type = self.initial_type
        final_type = self. final_type

        profile = (initial_type if initial_type.line_width > final_type.line_width else final_type).profile

        via = Via()
        (x_min, _), (x_max, _) = fp.get_bounding_box(via)
        w = x_max - x_min

        vias = fp.Device(
            name="VIA",
            content=[
                Vias(
                    width=w,
                    height=h,
                    spacing=spacing,
                    top_layer=self.top_layer,
                    via_layer=self.via_layer,
                    bottom_layer=self.bottom_layer,
                    transform=fp.translate(0, offset),
                )
                for _layer, offset_widths, _extension in profile
                for offsets, widths in offset_widths
                for h in widths
            ],
            ports=(),
        )

        curve_paint = fp.el.CurvePaint.PeriodicSampling(pattern=vias, period=w + spacing, reserved_ends=(w / 2 + spacing / 2, w / 2 + spacing / 2))
        extension = overlap / 2
        start = length - extension
        end = length + extension
        curve_length = curve.curve_length

        if start < 0 and end > curve_length:
            subcurve = curve.extended((extension, extension)).subcurve(start + extension, end + extension)
            paint = curve_paint(subcurve)
        elif end > curve_length:
            subcurve = curve.extended((0, extension)).subcurve(start , end)
            paint = curve_paint(subcurve)
        elif start < 0:
            subcurve = curve.extended((extension, 0)).subcurve(start + extension, end + extension)
            paint = curve_paint(subcurve)
        else:
            subcurve = curve.subcurve(start, end)
            paint = curve_paint(subcurve)

        return fp.Device(content=[paint], ports=initial_type.ports(subcurve, final_type=final_type)), (extension,extension)

def vias1(end_types: Tuple[fpt.IMetalLineType, fpt.IMetalLineType]) -> fpt.IViasFactory:
    a, b = end_types
    assert isinstance(a, CrackedMetalLineType) and isinstance(b, CrackedMetalLineType), f"Unsupported auto vias: [{a}] >> [{b}]"

    from SITRI_pdk.technology import get_technology
    TECH = get_technology()

    return _Vias(
        initial_type=a,
        final_type=b,
        top_layer=TECH.LAYER.MT2,
        via_layer=TECH.LAYER.VIA2,
        bottom_layer=TECH.LAYER.MT1,
    )

@dataclass(frozen=True)
class _Taper(fpt.IViasFactory):
    initial_type: CrackedMetalLineType
    final_type: CrackedMetalLineType

    def __call__(self, curve: fpt.ICurve, length: float) -> Tuple[fpt.IElement, Tuple[float, float]]:
        from SITRI_pdk.technology import get_technology

        TECH = get_technology()
        d = TECH.METRICS.GRID / 4
        subcurve = curve.subcurve(start=length, end=length + d) if length + d <= curve.curve_length else curve.subcurve(start=length - d, end=length)
        taper = fp.Device(content=[], ports=self.initial_type.ports(subcurve, final_type=self.final_type))
        return taper, (0, 0)

def taper(end_types: Tuple[fpt.IMetalLineType, fpt.IMetalLineType]) -> fpt.IViasFactory:
    a, b = end_types
    assert isinstance(a, CrackedMetalLineType) and isinstance(b, CrackedMetalLineType), f"Unsupported auto taper: [{a}] >> [{b}]"
    return _Taper(initial_type=a, final_type=b)

class AUTO_VIAS:
    @fpt.classconst
    @classmethod
    def DEFAULT(cls):
        return fpt.AutoVias().updated(
            [
                (METAL.MT2 >> METAL.MT1, vias1),
                (METAL.MT2 >> METAL.MT1, taper),

            ]
        )