from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional, Tuple

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt


@dataclass(frozen=True)
class SlotMetalLineType(fpt.MetalLineType):
    """Metal line with slot."""

    line_width: float
    port_names: Tuple[fpt.IPortOption, fpt.IPortOption] = field(default=("ep_0", "ep_1"), compare=False)
    max_width: float = 35
    slot_width: float = 3
    slot_length: float = 30
    min_slot_length: float = 30
    slot_gap: float = 10
    stagger_offset: float = 15

    def port_width(self) -> float:
        return self.line_width

    def __call__(
        self,
        curve: fpt.ICurve,
        *,
        offset: float = 0,
        final_offset: Optional[float] = None,
        extension: Tuple[float, float] = (0, 0),
    ) -> fpt.IMetalLineLike:
        curve_paint = fp.el.CurvePaint.Composite(
            (
                fp.el.CurvePaint.ContinuousLayer(layer=layer, offset=0, width=self.line_width, extension=extension).with_slots(
                    max_width=self.max_width,
                    slot_width=self.slot_width,
                    slot_length=self.slot_length,
                    min_slot_length=self.min_slot_length,
                    slot_gap=self.slot_gap,
                    stagger_offset=self.stagger_offset,
                )
                for layer in self.metal_stack.layers
            )
        )
        cell = curve_paint(curve, offset=offset, final_offset=final_offset, extension=extension).with_ports(
            *self.ports(curve, names=self.port_names, offset=offset, final_offset=final_offset)
        )
        return fpt.MetalLine(cell=cell, raw_curve=curve, type=self, offset=offset, final_offset=final_offset, extension=extension)


@dataclass(frozen=True)
class CrackedMetalLineType(fpt.ProfileMetalLineType):
    """Metal line with crack."""

    line_width: float
    port_names: Tuple[fpt.IPortOption, fpt.IPortOption] = field(default=("ep_0", "ep_1"), compare=False)

    max_width: float = 35
    spacing: float = 3

    @cached_property
    def profile(self):
        width = self.line_width
        max_width = self.max_width
        spacing = self.spacing
        return [
            (
                layer,
                fp.el.CurvePaint.ContinuousLayer(layer=layer, width=width).with_cracks(max_width=max_width, spacing=spacing).offset_widths(),
                (0, 0),
            )
            for layer in self.metal_stack.layers
        ]

    def port_width(self) -> float:
        return self.line_width
