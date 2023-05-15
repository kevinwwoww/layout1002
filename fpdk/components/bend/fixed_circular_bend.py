from dataclasses import dataclass
import math

from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk.util.json_cell import JsonCell

@dataclass(eq=False)
class FixedBendCircular_FWG_C_WIRE():