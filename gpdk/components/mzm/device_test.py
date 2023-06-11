import math
from dataclasses import dataclass
from typing import Tuple, cast
from fnpcell import all as fp
from gpdk.components.sbend.sbend_circular import SBendCircular
from gpdk.components.straight.straight import Straight
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType



@dataclass(eq=False)
class device(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()

        straight = Straight(length=10, waveguide_type=get_technology().WG.FWG.C.WIRE).translated(tx=-10, ty=-5)
        bend = SBendCircular()

        device = fp.Device(
            content=[straight,bend],
            ports=[straight["op_0"].with_name("op_0"), bend["op_1"]],
        )
        insts += device
        ports += device["op_0"].with_name("op_0")
        ports += device["op_1"].with_name("op_1")

        return insts, elems, ports





if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += device()

    # fmt: on
    # =============================================================
    # fp.export_gds(library, file=gds_file)
    fp.plot(library)
