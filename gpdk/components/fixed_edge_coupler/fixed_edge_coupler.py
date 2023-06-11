from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class Fixed_Edge_Coupler(fp.PCell):
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=1, default=["op_0"])

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off

        wg = TECH.WG.FWG.C.WIRE(curve=fp.g.Line(length=199, anchor=fp.Anchor.END, origin=(0, 0)))
        insts += wg
        ports += wg["op_1"].with_name(self.port_names[0])
        polygon2 = fp.el.Polygon([(-250, -50), (-200, -50), (-200, 50), (-250, 50)], layer=TECH.LAYER.DT_DRW)
        elems += polygon2
        polygon3 = fp.el.Polygon([(-200, -3), (-200, 3), (0, 1), (0, -1)], layer=TECH.LAYER.DEVREC_NOTE)
        elems += polygon3
        polygon4 = fp.el.Polygon([(-200, -20), (-200, 20), (0, 10.474), (0, -10.474)], layer=TECH.LAYER.M1KO_DRW)
        elems += polygon4
        rect = fp.el.Rect(width=50, height=100, center=(-225, 0), layer=TECH.LAYER.FIBTGT_NOTE)
        elems += rect
        text = fp.el.Text("optFiber", text_anchor=fp.Anchor.CENTER, vertical_align=fp.VertialAlign.MIDDLE, at=(-225, 0), layer=TECH.LAYER.FIBTGT_NOTE)
        elems += text

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += Fixed_Edge_Coupler()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
