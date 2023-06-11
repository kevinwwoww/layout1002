from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from fnpcell import all as fp

import IMECAS_SiN_pdk_1_0_0.util.curvature_util
from IMECAS_SiN_pdk_1_0_0.technology import get_technology
from IMECAS_SiN_pdk_1_0_0.util.json_cell import JsonCell
from functools import cached_property

@dataclass(eq=False)
class SIN_Bend_C(JsonCell, fp.IWaveguideLike, locked=True):

    @cached_property
    def raw_curve(self):
        curve = fp.g.EllipticalArc(radius=100, final_degrees=90)
        new_curve = curve.h_mirrored().translated(100+10.75, 0)

        return new_curve

    # @property
    # def radius_eff(self) -> float:
    #     return 100
    #
    # @property
    # def raw_curve(self):
    #     return fp.g.FakeCurve(self.cell["in1"], self.cell["out1"], curve_length=350)



@dataclass(eq=False)
class SIN_Bend_C_new(fp.IWaveguideLike, fp.PCell, locked=True):
    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        wg = SIN_Bend_C().h_mirrored()
        wg = wg["in1"].repositioned(at=(100, 0)).owner

        insts += wg
        ports += wg.ports
        return insts, elems, ports

    @cached_property
    def raw_curve(self):
        return fp.g.EllipticalArc(
            radius=100,
            final_degrees=90,
        )


if __name__ == "__main__":
    from IMECAS_SiN_pdk_1_0_0.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    # library += JsonCell(stem_name="SIN_Bend_C", root_folder=Path(__file__).parent)
    # library += SIN_Bend_C_new()
    library += SIN_Bend_C()


    fp.export_gds(library, file=gds_file)
    fp.plot(library)