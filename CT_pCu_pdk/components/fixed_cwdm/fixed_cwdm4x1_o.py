from dataclasses import dataclass
from pathlib import Path
from fnpcell import all as fp
from CT_pCu_pdk.technology import get_technology
from CT_pCu_pdk.util.json_cell import JsonCell

@dataclass(eq=False)
class cwdm4x1_o(JsonCell, locked=True):
    pass


if __name__ == "__main__":
    from CT_pCu_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += JsonCell(stem_name="cwdm4x1_o", root_folder=Path(__file__).parent)
    library += cwdm4x1_o()

    fp.export_gds(library, file=gds_file)