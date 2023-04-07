from abc import abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Callable, List, Optional, Sequence, Tuple, TypeVar

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt

_Self1 = TypeVar("_Self1", bound="CoreWaveguideType")


@dataclass(frozen=True)
class CoreWaveguideType(fpt.ProfileWaveguideType):
    """CT WG type, only core layer."""

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

    def updated(self: _Self1, **kwargs: Any) -> _Self1:
        if "wg_layout_width" not in kwargs:
            if "wg_design_width" in kwargs or ("wg_bias" in kwargs and self.wg_design_width is not None):
                kwargs["wg_layout_width"] = None
        return super().updated(**kwargs)


_Self2 = TypeVar("_Self2", bound="SlabWaveguideType")


@dataclass(frozen=True)
class SlabWaveguideType(fpt.ProfileWaveguideType):
    """CT slab WG type, hard_mask_wg + rib_wg + strip_wg ."""

    hm_layout_width: Optional[float] = None
    rib_layout_width: Optional[float] = None
    strip_layout_width: Optional[float] = None

    hm_design_width: Optional[float] = None
    rib_design_width: Optional[float] = None
    strip_design_width: Optional[float] = None

    port_names: Tuple[fpt.IPortOption, fpt.IPortOption] = field(default=("op_0", "op_1"), compare=False)

    def __post_init__(self):

        hm_design_width = self.hm_design_width
        rib_design_width = self.rib_design_width
        strip_design_width = self.strip_design_width
        if self.hm_layout_width is None and hm_design_width is not None:
            cd_bias = self.hm_bias(hm_design_width)
            object.__setattr__(self, "hm_layout_width", hm_design_width + cd_bias)
        assert self.hm_layout_width, "Either hm_design_width or hm_layout_width must be provided with a positive value"

        if self.rib_layout_width is None and rib_design_width is not None:
            cd_bias = self.rib_bias(rib_design_width)
            object.__setattr__(self, "rib_layout_width", rib_design_width + cd_bias)
        assert self.rib_layout_width, "Either rib_design_width or rib_layout_width must be provided with a positive value"

        if self.strip_layout_width is None and strip_design_width is not None:
            cd_bias = self.strip_bias(strip_design_width)
            object.__setattr__(self, "strip_layout_width", strip_design_width + cd_bias)
        assert self.strip_layout_width, "Either strip_design_width or strip_layout_width must be provided with a positive value"

    @property
    @abstractmethod
    def wg_layer(self) -> fpt.ILayer:
        ...

    @property
    @abstractmethod
    def rib_layer(self) -> fpt.ILayer:
        ...

    @property
    @abstractmethod
    def strip_layer(self) -> fpt.ILayer:
        ...

    @property
    def hm_width(self) -> float:
        assert self.hm_layout_width is not None
        return self.hm_layout_width

    @property
    def rib_width(self) -> float:
        assert self.rib_layout_width is not None
        return self.rib_layout_width

    @property
    def strip_width(self) -> float:
        assert self.strip_layout_width is not None
        return self.strip_layout_width

    @cached_property
    def hm_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    @cached_property
    def rib_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    @cached_property
    def strip_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    def port_width(self) -> float:
        return self.hm_width

    @cached_property
    def profile(self) -> Sequence[Tuple[fpt.ILayer, Sequence[Tuple[float, Sequence[float]]], Tuple[float, float]]]:
        return [
            (
                self.wg_layer,
                [
                    (0, [self.hm_width]),
                ],
                (0, 0),
            ),
            (
                self.rib_layer,
                [
                    (0, [self.hm_width, self.rib_width]),
                ],
                (0, 0),
            ),
            (
                self.strip_layer,
                [
                    (0, [self.hm_width, self.rib_width, self.strip_width]),
                ],
                (0, 0),
            ),
        ]

    def updated(self: _Self2, **kwargs: Any) -> _Self2:
        if "hm_layout_width" not in kwargs:
            if "hm_design_width" in kwargs or ("hm_bias" in kwargs and self.hm_design_width is not None):
                kwargs["hm_layout_width"] = None
        if "rib_layout_width" not in kwargs:
            if "rib_design_width" in kwargs or ("rib_bias" in kwargs and self.rib_design_width is not None):
                kwargs["rib_layout_width"] = None
        if "strip_layout_width" not in kwargs:
            if "strip_design_width" in kwargs or ("strip_bias" in kwargs and self.strip_design_width is not None):
                kwargs["strip_layout_width"] = None
        return super().updated(**kwargs)
