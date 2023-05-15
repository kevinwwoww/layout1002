from abc import abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Callable, List, Optional, Sequence, Tuple, TypeVar

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt

_Self1 = TypeVar("_Self1", bound="CoreCladdingWaveguideType")


@dataclass(frozen=True)
class CoreCladdingWaveguideType(fpt.ProfileWaveguideType):
    """Base class of waveguide type."""

    core_layout_width: Optional[float] = None
    cladding_layout_width: Optional[float] = None

    core_design_width: Optional[float] = None
    cladding_design_width: Optional[float] = None

    port_names: Tuple[fpt.IPortOption, fpt.IPortOption] = field(default=("op_0", "op_1"), compare=False)

    def __post_init__(self):
        """
        must be called using super() if subclass override it
        """
        core_design_width = self.core_design_width
        cladding_design_width = self.cladding_design_width
        if self.core_layout_width is None and core_design_width is not None:
            cd_bias = self.core_bias(core_design_width)
            object.__setattr__(self, "core_layout_width", core_design_width + cd_bias)
        assert self.core_layout_width, "Either core_design_width or core_layout_width must be provided with a positive value"

        if self.cladding_layout_width is None and cladding_design_width is not None:
            cd_bias = self.cladding_bias(cladding_design_width)
            object.__setattr__(self, "cladding_layout_width", cladding_design_width + cd_bias)
        assert self.cladding_layout_width is not None, "Either cladding_design_width or cladding_layout_width must be provided"

    @property
    @abstractmethod
    def core_layer(self) -> fpt.ILayer:
        ...

    @property
    @abstractmethod
    def cladding_layer(self) -> fpt.ILayer:
        ...

    @property
    def core_width(self) -> float:
        assert self.core_layout_width is not None
        return self.core_layout_width

    @property
    def cladding_width(self) -> float:
        assert self.cladding_layout_width is not None
        return self.cladding_layout_width

    @cached_property
    def core_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    @cached_property
    def cladding_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    def port_width(self) -> float:
        return self.core_width

    @cached_property
    def profile(self) -> Sequence[Tuple[fpt.ILayer, Sequence[Tuple[float, Sequence[float]]], Tuple[float, float]]]:
        return [
            (
                self.core_layer,
                [
                    (0, [self.core_width]),
                ],
                (0, 0),
            ),
            (
                self.cladding_layer,
                [
                    (0, [self.core_width, self.cladding_width]),
                ],
                (0, 0),
            ),
        ]

    def updated(self: _Self1, **kwargs: Any) -> _Self1:
        if "core_layout_width" not in kwargs:
            if "core_design_width" in kwargs or ("core_bias" in kwargs and self.core_design_width is not None):
                kwargs["core_layout_width"] = None
        if "cladding_layout_width" not in kwargs:
            if "cladding_design_width" in kwargs or ("cladding_bias" in kwargs and self.cladding_design_width is not None):
                kwargs["cladding_layout_width"] = None
        return super().updated(**kwargs)


_Self2 = TypeVar("_Self2", bound="SlotWaveguideType")


@dataclass(frozen=True)
class SlotWaveguideType(fpt.ProfileWaveguideType):

    core_layout_width: Optional[float] = None
    slot_layout_width: Optional[float] = None
    cladding_layout_width: Optional[float] = None

    core_design_width: Optional[float] = None
    slot_design_width: Optional[float] = None
    cladding_design_width: Optional[float] = None

    port_names: Tuple[fpt.IPortOption, fpt.IPortOption] = field(default=("op_0", "op_1"), compare=False)

    def __post_init__(self):
        """
        must be called using super() if subclass override it
        """
        core_design_width = self.core_design_width
        slot_design_width = self.slot_design_width
        cladding_design_width = self.cladding_design_width
        if self.core_layout_width is None and core_design_width is not None:
            cd_bias = self.core_bias(core_design_width)
            object.__setattr__(self, "core_layout_width", core_design_width + cd_bias)
        assert self.core_layout_width, "Either core_design_width or core_layout_width must be provided"

        if self.slot_layout_width is None and slot_design_width is not None:
            cd_bias = self.slot_bias(slot_design_width)
            object.__setattr__(self, "slot_layout_width", slot_design_width + cd_bias)
        assert self.slot_layout_width, "Either slot_design_width or slot_layout_width must be provided"

        if self.cladding_layout_width is None and cladding_design_width is not None:
            cd_bias = self.cladding_bias(cladding_design_width)
            object.__setattr__(self, "cladding_layout_width", cladding_design_width + cd_bias)
        assert self.cladding_layout_width, "Either cladding_design_width or cladding_layout_width must be provided"

    @property
    @abstractmethod
    def core_layer(self) -> fpt.ILayer:
        ...

    @property
    @abstractmethod
    def cladding_layer(self) -> fpt.ILayer:
        ...

    @property
    def core_width(self) -> float:
        assert self.core_layout_width is not None
        return self.core_layout_width

    @property
    def slot_width(self) -> float:
        assert self.slot_layout_width is not None
        return self.slot_layout_width

    @property
    def cladding_width(self) -> float:
        assert self.cladding_layout_width is not None
        return self.cladding_layout_width

    @cached_property
    def core_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    @cached_property
    def slot_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    @cached_property
    def cladding_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    def port_width(self) -> float:
        return self.core_width

    @cached_property
    def profile(self) -> Sequence[Tuple[fpt.ILayer, Sequence[Tuple[float, Sequence[float]]], Tuple[float, float]]]:
        """Return the waveguide profile

        format:
        profile = [layer_defs, layer_defs...]
        where layer_defs = (layer, [(offset, [width]), (offset, [width]), ...])
        if there's more than one width(to fix on-grid errors), please put them in ascend order
        """
        core_width = self.core_width
        slot_width = self.slot_width
        line_width = (core_width - slot_width) / 2
        return [
            (
                self.core_layer,
                [
                    (slot_width / 2 + line_width / 2, [line_width]),
                    (-slot_width / 2 - line_width / 2, [line_width]),
                ],
                (0, 0),
            ),
            (
                self.cladding_layer,
                [
                    (0, [slot_width, core_width, self.cladding_width]),
                ],
                (0, 0),
            ),
        ]

    def updated(self: _Self2, **kwargs: Any) -> _Self2:
        if "core_layout_width" not in kwargs:
            if "core_design_width" in kwargs or ("core_bias" in kwargs and self.core_design_width is not None):
                kwargs["core_layout_width"] = None
        if "slot_layout_width" not in kwargs:
            if "slot_design_width" in kwargs or ("slot_bias" in kwargs and self.slot_design_width is not None):
                kwargs["slot_layout_width"] = None
        if "cladding_layout_width" not in kwargs:
            if "cladding_design_width" in kwargs or ("cladding_bias" in kwargs and self.cladding_design_width is not None):
                kwargs["cladding_layout_width"] = None
        return super().updated(**kwargs)


@dataclass(frozen=True)
class SwgWaveguideType(CoreCladdingWaveguideType):
    # TODO what's the relations between PERIOD/DUTY_CYCLE and core_bias ?
    period: float = 1.0
    duty_cycle: float = 0.5

    port_names: Tuple[fpt.IPortOption, fpt.IPortOption] = field(default=("op_0", "op_1"), compare=False)

    def __call__(self, curve: fpt.ICurve, *, offset: float = 0, final_offset: Optional[float] = None) -> fpt.ICell:
        (
            (core_layer, ((core_offset, core_widths),), core_extension),
            (cladding_layer, ((cladding_offset, cladding_widths),), cladding_extension),
        ) = self.profile

        core_paint = fp.el.CurvePaint.from_profile([(core_layer, [(core_offset, core_widths)], core_extension)])
        cladding_paint = fp.el.CurvePaint.from_profile([(cladding_layer, [(cladding_offset, cladding_widths)], cladding_extension)])

        period = self.period
        duty_cycle = self.duty_cycle
        b = period * duty_cycle

        offsetted_curve = curve.offsetted(offset=offset, final_offset=final_offset)
        core: List[fpt.IElement] = []
        total_length = offsetted_curve.curve_length
        start = 0
        while start < total_length:
            core.append(core_paint(offsetted_curve.subcurve(start, min(start + b, total_length))))
            start += period

        cladding = cladding_paint(offsetted_curve)
        return fp.Composite(core, cladding).with_ports(*self.ports(curve, names=self.port_names, offset=offset, final_offset=final_offset))
