from dataclasses import dataclass
from pathlib import Path
from fnpcell import all as fp
from CT_Al_pdk.technology import get_technology
from CT_Al_pdk.util.json_cell import JsonCell

@dataclass(eq=False)
class fgc_si_al_c_tm(JsonCell, locked=True):
    pass


if __name__ == "__main__":
    from CT_Al_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += JsonCell(stem_name="fgc_si_al_c_tm", root_folder=Path(__file__).parent)
    library += fgc_si_al_c_tm()

    fp.export_gds(library, file=gds_file)