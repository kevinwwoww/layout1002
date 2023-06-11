from dataclasses import dataclass
from typing import Mapping, cast
import numpy as np
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.components.step.step2.mmi1x2 import MMI1x2

@dataclass(eq=False)
class OPA(fp.PCell):
    x_spacing: float = fp.PositiveFloatParam(default=50)
    end_y_spacing:float = fp.PositiveFloatParam(default=100)
    order: float = fp.PositiveFloatParam(default=3)

    def builf(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        x_spacing = self.x_spacing
        end_y_spacing = self.end_y_spacing
        order = self.order
        mmi = MMI1x2()
        num_per_col = []
        v_spacing = []

