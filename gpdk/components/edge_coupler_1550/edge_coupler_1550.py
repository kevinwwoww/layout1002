from dataclasses import dataclass

from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk.util.json_cell import JsonCell


@dataclass(eq=False)
class Edge_Coupler_1550(JsonCell, locked=True):
    """
    Examples:
    ```python
    ec = Edge_Coupler_1550()
    fp.plot(ec)
    ```
    """

    json_path: fp.StrPath = "./json_file/edge_coupler_1550.json"
    gds_path: fp.StrPath = "./gds_file/edge_coupler_1550.gds"


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += Edge_Coupler_1550()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
