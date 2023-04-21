from dataclasses import dataclass
from pathlib import Path
from fnpcell import all as fp
from AMFpdk_3_5_Oband.technology import get_technology
from AMFpdk_3_5_Oband.util.json_cell import JsonCell

@dataclass(eq=False)
class AMF_PSOI_PowMonitor_Oband_Cell_v3p5(JsonCell, locked=True):
    pass


if __name__ == "__main__":
    from AMFpdk_3_5_Oband.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += JsonCell(stem_name="AMF_PSOI_PowMonitor_Oband_Cell_v3p5", root_folder=Path(__file__).parent, gds_name="AMF_PSOI_Oband_merge_bb")
    library += AMF_PSOI_PowMonitor_Oband_Cell_v3p5()

    fp.export_gds(library, file=gds_file)