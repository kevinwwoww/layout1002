from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class Boolean(fp.IWaveguideLike, fp.PCell):
    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        rect = fp.el.Rect(width=10, height=5, center=(0,0), layer=TECH.LAYER.M1_DRW)
        elems += rect.translated(0, 0)
        circ = fp.el.Circle(radius=8, initial_degrees=0, final_degrees=180, layer=TECH.LAYER.M1_DRW)
        elems += circ.translated(0, 0)
        bool = rect - circ
        elems += bool.translated(20, 0)
        bool = rect & circ
        elems += bool.translated(-20, 0)
        bool = rect | circ
        elems += bool.translated(0, 20)
        bool = rect ^ circ
        elems += bool.translated(0, -20)

        return insts, elems, ports

if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += Boolean()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
