from dataclasses import dataclass
from pathlib import Path
from fnpcell import all as fp
from IMECAS_pdk.technology import get_technology
from IMECAS_pdk.util.json_cell import JsonCell


@dataclass(eq=False)
class LAT1500_R_C(JsonCell, locked=True):
    pass


if __name__ == "__main__":
    from IMECAS_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += JsonCell(stem_name="LAT1500_R_C", root_folder=Path(__file__).parent)
    library += LAT1500_R_C()

    fp.export_gds(library, file=gds_file)
