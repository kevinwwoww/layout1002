from abc import abstractmethod
from types import ModuleType
from typing import Iterable, Tuple, Union

from openpyxl import Workbook

from fnpcell.interfaces import IRunnable, IRunnableContainer


class ICheckRule(IRunnable):
    @abstractmethod
    def checked(self, pdk: ModuleType, workbook: Workbook, index: int) -> Tuple[str, str]:
        ...


_T = Union[None, ICheckRule, Iterable["_T"]]


class IRuleLib(IRunnableContainer[ICheckRule]):
    content: Tuple[ICheckRule, ...] = tuple()

    @abstractmethod
    def __add__(self, other: _T) -> "IRuleLib":
        ...

    @abstractmethod
    def check(self, pdk: ModuleType):
        ...
