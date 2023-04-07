from abc import abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Callable, List, Optional, Sequence, Tuple, TypeVar

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt

_Self3 = TypeVar("_Self3", bound="CoreWaveguideType")


@dataclass(frozen=True)
class CoreWaveguideType(fpt.ProfileWaveguideType):
    """AMF WG type, only core layer."""

    wg_layout_width: Optional[float] = None
    wg_design_width: Optional[float] = None

    port_names: Tuple[fpt.IPortOption, fpt.IPortOption] = field(default=("op_0", "op_1"), compare=False)

    def __post_init__(self):
        """
        must be called using super() if subclass override it
        """

        wg_design_width = self.wg_design_width
        if self.wg_layout_width is None and wg_design_width is not None:
            cd_bias = self.wg_bias(wg_design_width)
            object.__setattr__(self, "wg_layout_width", wg_design_width + cd_bias)
        assert self.wg_layout_width, "Either WG_design_width or WG_layout_width must be provided with a positive value"

    @property
    @abstractmethod
    def wg_layer(self) -> fpt.ILayer:
        ...

    @property
    def wg_width(self) -> float:
        assert self.wg_layout_width is not None
        return self.wg_layout_width

    @cached_property
    def wg_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    def port_width(self) -> float:
        return self.wg_width

    @cached_property
    def profile(self) -> Sequence[Tuple[fpt.ILayer, Sequence[Tuple[float, Sequence[float]]], Tuple[float, float]]]:
        return [
            (
                self.wg_layer,
                [
                    (0, [self.wg_width]),
                ],
                (0, 0),
            ),
        ]

    def updated(self: _Self3, **kwargs: Any) -> _Self3:
        if "wg_layout_width" not in kwargs:
            if "wg_design_width" in kwargs or ("wg_bias" in kwargs and self.wg_design_width is not None):
                kwargs["wg_layout_width"] = None
        return super().updated(**kwargs)


_Self4 = TypeVar("_Self4", bound="SlabWaveguideType")


@dataclass(frozen=True)
class SlabWaveguideType(fpt.ProfileWaveguideType):
    wg_rib_layout_width: Optional[float] = None
    wg_slab_layout_width: Optional[float] = None

    wg_rib_design_width: Optional[float] = None
    wg_slab_design_width: Optional[float] = None

    port_names: Tuple[fpt.IPortOption, fpt.IPortOption] = field(default=("op_0", "op_1"), compare=False)

    def __post_init__(self):

        wg_rib_design_width = self.wg_rib_design_width
        wg_slab_design_width = self.wg_slab_design_width
        if self.wg_rib_layout_width is None and wg_rib_design_width is not None:
            cd_bias = self.wg_rib_bias(wg_rib_design_width)
            object.__setattr__(self, "wg_rib_layout_width", wg_rib_design_width + cd_bias)
        assert self.wg_rib_layout_width, "Either wg_rib_design_width or wg_rib_layout_width must be provided with a positive value"

        if self.wg_slab_layout_width is None and wg_slab_design_width is not None:
            cd_bias = self.wg_slab_bias(wg_slab_design_width)
            object.__setattr__(self, "wg_slab_layout_width", wg_slab_design_width + cd_bias)
        assert self.wg_slab_layout_width is not None, "Either wg_slab_design_width or wg_slab_layout_width must be provided"

    @property
    @abstractmethod
    def wg_layer(self) -> fpt.ILayer:
        ...

    @property
    @abstractmethod
    def wg_slab_layer(self) -> fpt.ILayer:
        ...

    @property
    def wg_rib_width(self) -> float:
        assert self.wg_rib_layout_width is not None
        return self.wg_rib_layout_width

    @property
    def wg_slab_width(self) -> float:
        assert self.wg_slab_layout_width is not None
        return self.wg_slab_layout_width

    @cached_property
    def wg_rib_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    @cached_property
    def wg_slab_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    def port_width(self) -> float:
        return self.wg_rib_width

    @cached_property
    def profile(self) -> Sequence[Tuple[fpt.ILayer, Sequence[Tuple[float, Sequence[float]]], Tuple[float, float]]]:

        wg_rib_width = self.wg_rib_width
        wg_slab_width = self.wg_slab_width
        line_width = (wg_slab_width - wg_rib_width) / 2
        return [
            (
                self.wg_layer,
                [
                    (0, [wg_rib_width])
                ],
                (0, 0),
            ),
            (
                self.wg_slab_layer,
                [
                    (0, [wg_rib_width, wg_slab_width]),
                ],
                (0, 0),
            ),
        ]

    def updated(self: _Self4, **kwargs: Any) -> _Self4:
        if "wg_rib_layout_width" not in kwargs:
            if "wg_rib_design_width" in kwargs or ("wg_rib_bias" in kwargs and self.wg_rib_design_width is not None):
                kwargs["wg_rib_layout_width"] = None
        if "wg_slab_layout_width" not in kwargs:
            if "wg_slab_design_width" in kwargs or ("wg_slab_bias" in kwargs and self.wg_slab_design_width is not None):
                kwargs["wg_slab_layout_width"] = None
        return super().updated(**kwargs)
