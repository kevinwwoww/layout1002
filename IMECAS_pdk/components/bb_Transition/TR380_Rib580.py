from dataclasses import dataclass
from pathlib import Path
from fnpcell import all as fp
from IMECAS_pdk.technology import get_technology
from IMECAS_pdk.util.json_cell import JsonCell
from functools import cached_property


@dataclass(eq=False)
class TR380_Rib580(JsonCell, fp.ICurvedCellRef, locked=True):


    @cached_property
    def raw_curve(self):
        IN, OUT = self.cell.ports
        return fp.g.LineBetween(IN.position, OUT.position)


if __name__ == "__main__":
    from IMECAS_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += JsonCell(stem_name="TR380_Rib580", root_folder=Path(__file__).parent)
    library += TR380_Rib580()

    fp.export_gds(library, file=gds_file)
    fp.plot(library, title="TR380_Rib580")
