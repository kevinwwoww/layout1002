from dataclasses import dataclass
from pathlib import Path
from fnpcell import all as fp
from AMFpdk.technology import get_technology
from AMFpdk.util.json_cell import JsonCell


@dataclass(eq=False)
class Fixed_voa_al_c(JsonCell, locked=True):
    pass


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += JsonCell(stem_name="Fixed_voa_al_c", root_folder=Path(__file__).parent)
    library += Fixed_voa_al_c()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
