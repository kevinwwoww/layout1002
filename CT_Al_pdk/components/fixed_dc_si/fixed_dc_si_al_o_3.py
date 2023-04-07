from dataclasses import dataclass
from pathlib import Path
from fnpcell import all as fp
from CT_Al_pdk.technology import get_technology
from CT_Al_pdk.util.json_cell import JsonCell

@dataclass(eq=False)
class dc_si_al_o_3(JsonCell, locked=True):
    pass


if __name__ == "__main__":
    from CT_Al_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += JsonCell(stem_name="dc_si_al_o_3", root_folder=Path(__file__).parent)
    library += dc_si_al_o_3()

    fp.export_gds(library, file=gds_file)