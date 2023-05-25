from dataclasses import dataclass
from pathlib import Path
from fnpcell import all as fp
from SITRI_pdk.technology import get_technology
from SITRI_pdk.util.json_cell import JsonCell

@dataclass(eq=False)
class AMF_PSOI_PSiN1X2MMI_Cband_v3p1(JsonCell, locked=True):
    pass


if __name__ == "__main__":
    from SITRI_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += JsonCell(stem_name="AMF_PSOI_PSiN1X2MMI_Cband_v3p1", root_folder=Path(__file__).parent, gds_name="AMF_PSOI_Cband_merge_bb")
    library += AMF_PSOI_PSiN1X2MMI_Cband_v3p1()

    fp.export_gds(library, file=gds_file)