from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp

from AMFpdk.components.straight.straight import Straight
from AMFpdk.components.transition.slab2grat_transition import SLAB2GRATTransition
from AMFpdk.components.transition.slab2rib_transition import SLAB2RIBTransition
from AMFpdk.technology import WG, get_technology

@dataclass(eq=False)
class GRAT2RIBTransition(fp.ICurvedCellRef, fp.PCell):
    grat_length: float = fp.PositiveFloatParam(default=20)
    grat_wire_only_length: float = fp.PositiveFloatParam(default=5.0)
    grat_deep_only_width: float = fp.PositiveFloatParam(default=3.0)
    grat_type: WG.GRAT.C = fp.WaveguideTypeParam(type=WG.GRAT.C)
    rib_length: float = fp.PositiveFloatParam(default=20)
    rib_wire_only_length: float = fp.PositiveFloatParam(default=5.0)
    rib_deep_only_width: float = fp.PositiveFloatParam(default=3.0)
    rib_type: WG.RIB.C = fp.WaveguideTypeParam(type=WG.RIB.C)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_grat_type(self):
        return get_technology().WG.GRAT.C.WIRE

    def _default_rib_type(self):
        return get_technology().WG.RIB.C.WIRE


    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        grat_length = self.grat_length
        grat_wire_only_length = self.grat_wire_only_length
        grat_deep_only_width = self.grat_deep_only_width
        grat_type = self.grat_type
        rib_length = self.rib_length
        rib_wire_only_length = self.rib_wire_only_length
        rib_deep_only_width = self.rib_deep_only_width
        rib_type = self.rib_type
        anchor = self.anchor
        port_names = self.port_names
        straight_length = 5
        total_length = grat_length + straight_length + rib_length
        tx = 0

        if anchor == fp.Anchor.END:
            tx = -total_length
        elif anchor == fp.Anchor.CENTER:
            tx = -total_length / 2
        transform = fp.translate(tx, 0)

        slab2grat = SLAB2GRATTransition(
            name="grat",
            length=grat_length,
            wire_only_length=grat_wire_only_length,
            deep_only_width=grat_deep_only_width,
            slab_type=TECH.WG.SLAB.C.WIRE,
            grat_type=grat_type,
            transform=fp.rotate(degrees=180).translate(-straight_length / 2, 0) @transform,
        )

        insts += slab2grat
        ports += slab2grat["op_1"].with_name(port_names[0])
        straight = Straight(
            name="straight",
            length=straight_length,
            waveguide_type=TECH.WG.SLAB.C.WIRE,
            anchor=fp.Anchor.CENTER,
            transform=transform,
        )
        insts += straight
        slab2rib = SLAB2RIBTransition(
            name="rib",
            length=rib_length,
            wire_only_length=rib_wire_only_length,
            deep_only_width=rib_deep_only_width,
            slab_type=TECH.WG.SLAB.C.WIRE,
            rib_type=rib_type,
            transform=fp.translate(straight_length / 2, 0) @ transform,
        )
        insts += slab2rib
        ports += slab2rib["op_1"].with_name(port_names[1])

        return insts, elems, ports

    @property
    def raw_curve(self):
        IN, OUT = self.cell.ports
        return fp.g.LineBetween(IN.position, OUT.position)


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += GRAT2RIBTransition()



    fp.export_gds(library, file=gds_file)