from dataclasses import dataclass
from pathlib import Path
from fnpcell import all as fp
from IMECAS_SiN_pdk.technology import get_technology
from IMECAS_SiN_pdk.util.json_cell import JsonCell


@dataclass(eq=False)
class SIN_YBranch_TE_C(JsonCell, locked=True):
    pass


if __name__ == "__main__":
    from IMECAS_SiN_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += JsonCell(stem_name="SIN_YBranch_TE_C", root_folder=Path(__file__).parent)
    library += SIN_YBranch_TE_C()

    fp.export_gds(library, file=gds_file)
