from fnpcell import all as fp
from dataclasses import dataclass


@dataclass(eq=False)
class PCellCustom(fp.PCell):
    name: str = fp.NameParam(prefix="", hash=False, compare=False)
