from fnpcell import all as fp
from gpdk.technology import get_technology


if __name__ == "__main__":
    from pathlib import Path
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += fp.import_from_json(json_path=Path(__file__).with_name("MH_TE_1550.json"))

    # fmt: on
    # =============================================================
    #  fp.plot(library)
    fp.export_gds(library, file=gds_file)
