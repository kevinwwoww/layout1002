from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk.technology import get_technology

@dataclass(eq=False)
class Fixed_Edge_Coupler(fp.PCell):
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=1, default=["op_0"])

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        wg = TECH.WG.CHANNEL.C.WIRE(curve=fp.g.Line(length=199, anchor=fp.Anchor.END, origin=(0, 0)))
        insts += wg
        ports += wg["op_1"].with_name(self.port_names[0])

        polygon2 = fp.el.Polygon([(-250, -50), (-200, -50), (-200, 50), (-250, 50)], layer=TECH.LAYER.DT)
        elems += polygon2

        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file
    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += Fixed_Edge_Coupler()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)