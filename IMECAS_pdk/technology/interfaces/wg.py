from abc import abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Callable, List, Optional, Sequence, Tuple, TypeVar

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt

_Self1 = TypeVar("_Self1", bound="CoreCladdingWaveguideType")


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
                    (0, [self.core_width, self.cladding_width, self.trench_width])
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


_Self2 = TypeVar("_Self2", bound="Core2Cladding2WaveguideType")


@dataclass(frozen=True)
class Core2Cladding2WaveguideType(fpt.ProfileWaveguideType):
    core1_layout_width: Optional[float] = None
    cladding1_layout_width: Optional[float] = None
    core2_layout_width: Optional[float] = None
    cladding2_layout_width: Optional[float] = None

    core1_design_width: Optional[float] = None
    cladding1_design_width: Optional[float] = None
    core2_design_width: Optional[float] = None
    cladding2_design_width: Optional[float] = None

    port_names: Tuple[fpt.IPortOption, fpt.IPortOption] = field(default=("op_0", "op_1"), compare=False)

    def __post_init__(self):
        """
        must be called using super() if subclass override it
        """
        core1_design_width = self.core1_design_width
        cladding1_design_width = self.cladding1_design_width
        core2_design_width = self.core2_design_width
        cladding2_design_width = self.cladding2_design_width

        if self.core1_layout_width is None and core1_design_width is not None:
            cd_bias = self.core1_bias(core1_design_width)
            object.__setattr__(self, "core1_layout_width", core1_design_width + cd_bias)
        assert self.core1_layout_width, "Either core1_design_width or core1_layout_width must be provided with a positive value"

        if self.cladding1_layout_width is None and cladding1_design_width is not None:
            cd_bias = self.cladding1_bias(cladding1_design_width)
            object.__setattr__(self, "cladding1_layout_width", cladding1_design_width + cd_bias)
        assert self.cladding1_layout_width is not None, "Either cladding1_design_width or cladding1_layout_width must be provided"

        if self.core2_layout_width is None and core2_design_width is not None:
            cd_bias = self.core2_bias(core2_design_width)
            object.__setattr__(self, "core2_layout_width", core2_design_width + cd_bias)
        assert self.core2_layout_width, "Either core2_design_width or core2_layout_width must be provided with a positive value"

        if self.cladding2_layout_width is None and cladding2_design_width is not None:
            cd_bias = self.cladding2_bias(cladding2_design_width)
            object.__setattr__(self, "cladding2_layout_width", cladding2_design_width + cd_bias)
        assert self.cladding2_layout_width is not None, "Either cladding2_design_width or cladding2_layout_width must be provided"

    @property
    @abstractmethod
    def core1_layer(self) -> fpt.ILayer:
        ...

    @property
    @abstractmethod
    def cladding1_layer(self) -> fpt.ILayer:
        ...

    @property
    @abstractmethod
    def core_layer(self) -> fpt.ILayer:
        ...

    @property
    @abstractmethod
    def cladding_layer(self) -> fpt.ILayer:
        ...

    @property
    def core1_width(self) -> float:
        assert self.core1_layout_width is not None
        return self.core1_layout_width

    @property
    def cladding1_width(self) -> float:
        assert self.cladding1_layout_width is not None
        return self.cladding1_layout_width

    @property
    def core2_width(self) -> float:
        assert self.core2_layout_width is not None
        return self.core2_layout_width

    @property
    def cladding2_width(self) -> float:
        assert self.cladding2_layout_width is not None
        return self.cladding2_layout_width

    @cached_property
    def core1_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    @cached_property
    def cladding1_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    @cached_property
    def core2_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    @cached_property
    def cladding2_bias(self) -> Callable[[float], float]:
        return fpt.CDBiasLinear(0)

    def port_width(self) -> float:
        return self.core2_width

    @cached_property
    def profile(self) -> Sequence[Tuple[fpt.ILayer, Sequence[Tuple[float, Sequence[float]]], Tuple[float, float]]]:
        return [
            (
                self.core1_layer,
                [
                    (0, [self.core1_width]),
                ],
                (0, 0),
            ),
            (
                self.cladding1_layer,
                [
                    (0, [self.core1_width, self.cladding1_width]),
                ],
                (0, 0),
            ),
            (
                self.core_layer,
                [
                    (0, [self.core2_width]),
                ],
                (0, 0),
            ),
            (
                self.cladding_layer,
                [
                    (0, [self.core2_width, self.cladding2_width]),
                ],
                (0, 0),
            ),
        ]

    def updated(self: _Self1, **kwargs: Any) -> _Self1:
        if "core1_layout_width" not in kwargs:
            if "core1_design_width" in kwargs or ("core1_bias" in kwargs and self.core1_design_width is not None):
                kwargs["core1_layout_width"] = None
        if "cladding1_layout_width" not in kwargs:
            if "cladding1_design_width" in kwargs or (
                    "cladding1_bias" in kwargs and self.cladding1_design_width is not None):
                kwargs["cladding1_layout_width"] = None
        if "core2_layout_width" not in kwargs:
            if "core2_design_width" in kwargs or ("core2_bias" in kwargs and self.core2_design_width is not None):
                kwargs["core2_layout_width"] = None
        if "cladding2_layout_width" not in kwargs:
            if "cladding2_design_width" in kwargs or (
                    "cladding2_bias" in kwargs and self.cladding2_design_width is not None):
                kwargs["cladding2_layout_width"] = None
        return super().updated(**kwargs)
