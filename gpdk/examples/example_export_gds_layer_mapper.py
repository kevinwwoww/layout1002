from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class Rects(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()

        elems += fp.el.Rect(width=2, height=2, center=(0, 0), layer=TECH.LAYER.ERROR_MARK)
        elems += fp.el.Rect(width=2, height=2, center=(0, 0), layer=TECH.LAYER.FLYLINE_MARK)
        elems += fp.el.Rect(width=2, height=2, center=(0, 0), layer=TECH.LAYER.TEXT_NOTE)
        elems += fp.el.Rect(width=2, height=2, center=(0, 0), layer=TECH.LAYER.PINREC_FWG).translated(0, 4)
        elems += fp.el.Rect(width=2, height=2, center=(0, 0), layer=TECH.LAYER.PINREC_MWG).translated(4, 0)
        elems += fp.el.Rect(width=2, height=2, center=(0, 0), layer=TECH.LAYER.PINREC_SWG).translated(4, 4)

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += Rects().with_name("TOP")

    # fmt: on
    # =============================================================
    layer_mapping = {  # map layer to target layer
        TECH.LAYER.TEXT_NOTE.value: TECH.LAYER.DEVREC_NOTE.value,
        TECH.LAYER.PINREC_FWG.value: TECH.LAYER.DEVREC_NOTE.value,
        (70, 33): TECH.LAYER.DEVREC_NOTE.value,
    }

    def layer_mapper(layer: Tuple[int, int]):
        if layer == TECH.LAYER.ERROR_MARK.value:  # TECH.LAYER.ERROR_MARK.value == (92, 35)
            return None  # remove this layer from result gds file
        if layer == (91, 35):  # (91, 35) == TECH.LAYER.FLYLINE_MARK.value
            return None  # remove this layer from result gds file
        if layer == (70, 32):  # map (70, 32) to (80, 30)
            return (80, 30)

        mapped_layer = layer_mapping.get(layer)  # lookup mapping dict. Sometime using dict is more convenient than using many if.
        if mapped_layer is not None:  # mapping exists
            return mapped_layer
        return layer  # fallback to original layer

    fp.export_gds(
        library,
        file=gds_file,
        layer_mapper=layer_mapper,
    )
