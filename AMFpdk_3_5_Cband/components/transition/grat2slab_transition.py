from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp

from AMFpdk.components.straight.straight import Straight
from AMFpdk.components.transition.rib2grat_transition import RIB2GRATTransition
from AMFpdk.components.transition.rib2slab_transition import RIB2SLABTransition
from AMFpdk.technology import WG, get_technology

@dataclass(eq=False)
class GRAT2SLABTransition(fp.ICurvedCellRef, fp.PCell):
    grat_length: float = fp.PositiveFloatParam(default=20)
    grat_wire_only_length: float = fp.PositiveFloatParam(default=5.0)
    grat_deep_only_width: float = fp.PositiveFloatParam(default=3.0)
    grat_type: WG.GRAT.C = fp.WaveguideTypeParam(type=WG.GRAT.C)
    slab_length: float = fp.PositiveFloatParam(default=20)
    slab_wire_only_length: float = fp.PositiveFloatParam(default=5.0)
    slab_deep_only_width: float = fp.PositiveFloatParam(default=3.0)
    slab_type: WG.RIB.C = fp.WaveguideTypeParam(type=WG.SLAB.C)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_grat_type(self):
        return get_technology().WG.GRAT.C.WIRE

    def _default_slab_type(self):
        return get_technology().WG.SLAB.C.WIRE


    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        grat_length = self.grat_length
        grat_wire_only_length = self.grat_wire_only_length
        grat_deep_only_width = self.grat_deep_only_width
        grat_type = self.grat_type
        slab_length = self.slab_length
        slab_wire_only_length = self.slab_wire_only_length
        slab_deep_only_width = self.slab_deep_only_width
        slab_type = self.slab_type
        anchor = self.anchor
        port_names = self.port_names
        straight_length = 5
        total_length = grat_length + straight_length + slab_length
        tx = 0

        if anchor == fp.Anchor.END:
            tx = -total_length
        elif anchor == fp.Anchor.CENTER:
            tx = -total_length / 2
        transform = fp.translate(tx, 0)

        rib2grat = RIB2GRATTransition(
            name="grat",
            length=grat_length,
            wire_only_length=grat_wire_only_length,
            deep_only_width=grat_deep_only_width,
            rib_type=TECH.WG.RIB.C.WIRE,
            grat_type=grat_type,
            transform=fp.rotate(degrees=180).translate(-straight_length / 2, 0) @transform,
        )

        insts += rib2grat
        ports += rib2grat["op_1"].with_name(port_names[0])
        straight = Straight(
            name="straight",
            length=straight_length,
            waveguide_type=TECH.WG.RIB.C.WIRE,
            anchor=fp.Anchor.CENTER,
            transform=transform,
        )
        insts += straight
        rib2slab = RIB2SLABTransition(
            name="slab",
            length=slab_length,
            wire_only_length=slab_wire_only_length,
            deep_only_width=slab_deep_only_width,
            rib_type=TECH.WG.RIB.C.WIRE,
            slab_type=slab_type,
            transform=fp.translate(straight_length / 2, 0) @ transform,
        )
        insts += rib2slab
        ports += rib2slab["op_1"].with_name(port_names[1])

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

    library += GRAT2SLABTransition()



    fp.export_gds(library, file=gds_file)