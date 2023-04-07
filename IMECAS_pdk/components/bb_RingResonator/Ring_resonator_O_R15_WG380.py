from dataclasses import dataclass
from pathlib import Path
from fnpcell import all as fp
from IMECAS_pdk.technology import get_technology
from IMECAS_pdk.util.json_cell import JsonCell


@dataclass(eq=False)
class Ring_resonator_O_R15_WG380(JsonCell, locked=True):
    pass


if __name__ == "__main__":
    from IMECAS_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += JsonCell(stem_name="Ring_resonator_O_R15_WG380", root_folder=Path(__file__).parent)
    library += Ring_resonator_O_R15_WG380()

    fp.export_gds(library, file=gds_file)
