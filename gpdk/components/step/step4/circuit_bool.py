from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology
from step.step3.mzi_target_length import MZI

@dataclass(eq=False)
class CircuitBool(fp.IWaveguideLike, fp.PCell):
    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        device = MZI()
        ports += device.ports
        insts += device
        cor = device.polygon_set(layer=TECH.LAYER.FWG_COR)
        # elems += cor
        cld = device.polygon_set(layer=TECH.LAYER.FWG_CLD)
        tre = fp.el.PolygonSet.boolean_sub(cld, cor, layer=TECH.LAYER.FWG_TRE)
        elems += tre.translated(0, -500)

        return insts, elems, ports

if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += CircuitBool()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
