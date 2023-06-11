from dataclasses import dataclass
from typing import List, Tuple, cast

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt

from .interfaces import CrackedMetalLineType
from .metal import METAL


@dataclass(frozen=True)
class _Vias(fpt.IViasFactory):
    initial_type: CrackedMetalLineType
    final_type: CrackedMetalLineType
    top_layer: fpt.ILayer
    via_layer: fpt.ILayer
    bottom_layer: fpt.ILayer

    def __call__(self, curve: fpt.ICurve, length: float) -> Tuple[fpt.IElement, Tuple[float, float]]:
        from ..components.via.via import Via
        from ..components.via.vias import Vias
        from . import get_technology

        TECH = get_technology()
        spacing = TECH.VIAS.SPACING
        overlap = TECH.VIAS.OVERLAP
        initial_type = self.initial_type
        final_type = self.final_type

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
                for _layer, offset_widths, _extension in profile  # we known each MetalLineType in GPDK has only one layer
                for offset, widths in offset_widths
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
            subcurve = curve.extended((0, extension)).subcurve(start, end)
            paint = curve_paint(subcurve)
        elif start < 0:
            subcurve = curve.extended((extension, 0)).subcurve(start + extension, end + extension)
            paint = curve_paint(subcurve)
        else:
            subcurve = curve.subcurve(start, end)
            paint = curve_paint(subcurve)

        return fp.Device(content=[paint], ports=initial_type.ports(subcurve, final_type=final_type)), (extension, extension)


def vias1(end_types: Tuple[fpt.IMetalLineType, fpt.IMetalLineType]) -> fpt.IViasFactory:
    a, b = end_types
    assert isinstance(a, CrackedMetalLineType) and isinstance(b, CrackedMetalLineType), f"Unsupported auto vias: [{a}] >> [{b}]"
    from . import get_technology

    TECH = get_technology()

    return _Vias(
        initial_type=a,
        final_type=b,
        top_layer=TECH.LAYER.M2_DRW,
        via_layer=TECH.LAYER.VIA1_DRW,
        bottom_layer=TECH.LAYER.M1_DRW,
    )


def vias2(end_types: Tuple[fpt.IMetalLineType, fpt.IMetalLineType]) -> fpt.IViasFactory:
    a, b = end_types
    assert isinstance(a, CrackedMetalLineType) and isinstance(b, CrackedMetalLineType), f"Unsupported auto vias: [{a}] >> [{b}]"
    from . import get_technology

    TECH = get_technology()
    return _Vias(
        initial_type=a,
        final_type=b,
        top_layer=TECH.LAYER.MT_DRW,
        via_layer=TECH.LAYER.VIA2_DRW,
        bottom_layer=TECH.LAYER.M2_DRW,
    )


@dataclass(frozen=True)
class _MultiLayerVias(fpt.IViasFactory):
    factories: Tuple[_Vias, ...]

    def __call__(self, curve: fpt.ICurve, length: float) -> Tuple[fpt.IElement, Tuple[float, float]]:
        factories = self.factories
        extension_start = 0
        extension_end = 0
        devices: List[fp.IDevice] = []
        for vias in factories:
            device, (es, ee) = vias(curve, length)
            devices.append(cast(fp.IDevice, device))
            extension_start = max(extension_start, es)
            extension_end = max(extension_end, ee)

        return fp.Device(content=devices, ports=[devices[0].ports[0], devices[-1].ports[-1]]), (
            extension_start,
            extension_end,
        )


def vias12(end_types: Tuple[fpt.IMetalLineType, fpt.IMetalLineType]) -> fpt.IViasFactory:
    a, b = end_types
    assert isinstance(a, CrackedMetalLineType) and isinstance(b, CrackedMetalLineType), f"Unsupported auto vias: [{a}] >> [{b}]"
    from . import get_technology

    TECH = get_technology()
    inter_metal_type = TECH.METAL.M2.W10  # just demo
    return _MultiLayerVias(
        factories=(
            _Vias(
                initial_type=a,
                final_type=inter_metal_type,
                top_layer=TECH.LAYER.MT_DRW,
                via_layer=TECH.LAYER.VIA2_DRW,
                bottom_layer=TECH.LAYER.M2_DRW,
            ),
            _Vias(
                initial_type=inter_metal_type,
                final_type=b,
                top_layer=TECH.LAYER.M2_DRW,
                via_layer=TECH.LAYER.VIA1_DRW,
                bottom_layer=TECH.LAYER.M1_DRW,
            ),
        )
    )


@dataclass(frozen=True)
class _Taper(fpt.IViasFactory):
    initial_type: CrackedMetalLineType
    final_type: CrackedMetalLineType

    def __call__(self, curve: fpt.ICurve, length: float) -> Tuple[fpt.IElement, Tuple[float, float]]:
        from . import get_technology

        TECH = get_technology()
        # d = TECH.METRICS.GRID / 4
        d = 100
        subcurve = curve.subcurve(start=length, end=length + d) if length + d <= curve.curve_length else curve.subcurve(start=length - d, end=length)
        taper = fp.Device(content=[], ports=self.initial_type.ports(subcurve, final_type=self.final_type))
        return taper, (0, 0)  # just fake it


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
                (METAL.MT >> METAL.M2, vias2),
                (METAL.M2 >> METAL.M1, vias1),
                (METAL.MT >> METAL.M1, vias12),
                #
                (METAL.MT >> METAL.MT, taper),
                (METAL.M2 >> METAL.M2, taper),
                (METAL.M1 >> METAL.M1, taper),
            ]
        )
