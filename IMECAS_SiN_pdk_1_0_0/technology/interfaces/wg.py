from abc import abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Callable, List, Optional, Sequence, Tuple, TypeVar

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt

_Self1 = TypeVar("_Self1", bound="CoreCladdingTrenchWaveguideType")


@dataclass(frozen=True)
class CoreCladdingTrenchWaveguideType(fpt.ProfileWaveguideType):
    """Base class of waveguide type."""

    core_layout_width: Optional[float] = None
    cladding_layout_width: Optional[float] = None
    trench_layout_width: Optional[float] = None

    core_design_width: Optional[float] = None
    cladding_design_width: Optional[float] = None
    trench_design_width: Optional[float] = None

    port_names: Tuple[fpt.IPortOption, fpt.IPortOption] = field(default=("op_0", "op_1"), compare=False)

    def __post_init__(self):
        """
        must be called using super() if subclass override it
        """
        core_design_width = self.core_design_width
        cladding_design_width = self.cladding_design_width
        trench_design_width = self.trench_design_width
        if self.core_layout_width is None and core_design_width is not None:
            cd_bias = self.core_bias(core_design_width)
            object.__setattr__(self, "core_layout_width", core_design_width + cd_bias)
        assert self.core_layout_width, "Either core_design_width or core_layout_width must be provided with a positive value"

        if self.cladding_layout_width is None and cladding_design_width is not None:
            cd_bias = self.cladding_bias(cladding_design_width)
            object.__setattr__(self, "cladding_layout_width", cladding_design_width + cd_bias)
        assert self.cladding_layout_width is not None, "Either cladding_design_width or cladding_layout_width must be provided"

        if self.trench_layout_width is None and trench_design_width is not None:
            cd_bias = self.trench_bias(trench_design_width)
            object.__setattr__(self, "trench_layout_width", trench_design_width + cd_bias)
        assert self.trench_layout_width is not None, "Either trench_design_width or trench_layout_width must be provided"

    @property
    @abstractmethod
    def core_layer(self) -> fpt.ILayer:
        ...

    @property
    @abstractmethod
    def cladding_layer(self) -> fpt.ILayer:
        ...

    @property
    @abstractmethod
    def trench_layer(self) -> fpt.ILayer:
        ...

    @property
    def core_width(self) -> float:
        assert self.core_layout_width is not None
        return self.core_layout_width

    @property
    def cladding_width(self) -> float:
        assert self.cladding_layout_width is not None
        return self.cladding_layout_width

    @property
    def trench_width(self) -> float:
        assert self.trench_layout_width is not None
        return self.trench_layout_width

    @cached_property
    def core_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    @cached_property
    def cladding_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    @cached_property
    def trench_bias(self) -> Callable[[float], float]:
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
            (
                self.trench_layer,
                [
                    (self.core_width / 2 + self.trench_width / 2, [self.trench_width]),
                    (-self.core_width / 2 - self.trench_width / 2, [self.trench_width]),
                ],
                (0, 0),
            ),
        ]

    def updated(self: _Self1, **kwargs: Any) -> _Self1:
        if "core_layout_width" not in kwargs:
            if "core_design_width" in kwargs or ("core_bias" in kwargs and self.core_design_width is not None):
                kwargs["core_layout_width"] = None
        if "cladding_layout_width" not in kwargs:
            if "cladding_design_width" in kwargs or (
                    "cladding_bias" in kwargs and self.cladding_design_width is not None):
                kwargs["cladding_layout_width"] = None
        if "trench_layout_width" not in kwargs:
            if "trench_design_width" in kwargs or ("trench_bias" in kwargs and self.trench_design_width is not None):
                kwargs["trench_layout_width"] = None
        return super().updated(**kwargs)





