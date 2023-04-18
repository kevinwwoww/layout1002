from dataclasses import dataclass
from pathlib import Path
from fnpcell import all as fp
from AMFpdk_3_5_Cband.technology import get_technology
from AMFpdk_3_5_Cband.util.json_cell import JsonCell

@dataclass(eq=False)
class AMF_PSOI_PSiNGC_Cband_preview(JsonCell, locked=True):
    pass


if __name__ == "__main__":
    from AMFpdk_3_5_Cband.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += JsonCell(stem_name="AMF_PSOI_PSiNGC_Cband_preview", root_folder=Path(__file__).parent, gds_name="AMF_PSOI_Cband_merge_bb")
    library += AMF_PSOI_PSiNGC_Cband_preview()

    fp.export_gds(library, file=gds_file)