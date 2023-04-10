from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk_3_5_Cband.components.transition._rib_transition import RIBtransition
from AMFpdk_3_5_Cband.technology import get_technology, WG

@dataclass(eq=False)
class RIB2GRATTransition(fp.ICurvedCellRef, fp.PCell):
    length: float = fp.PositiveFloatParam(default=20, doc="Length of transition")
    wire_only_length: float = fp.PositiveFloatParam(default=5.0, doc="Length of transition where shallow part is built up")
    deep_only_width: float = fp.PositiveFloatParam(default=3.0, doc="Core width of the waveguide at the end of shallow transition part")
    rib_type: WG.RIB.C = fp.WaveguideTypeParam(type=WG.RIB.C)
    grat_type: WG.GRAT.C = fp.WaveguideTypeParam(type=WG.GRAT.C)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])


    def _default_rib_type(self):
        return get_technology().WG.RIB.C.WIRE

    def _default_grat_type(self):
        return get_technology().WG.GRAT.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        transition = RIBtransition(
            length=self.length,
            wire_only_length=self.wire_only_length,
            deep_only_width=self.deep_only_width,
            rib_type=self.rib_type,
            other_type=self.grat_type,
            anchor=self.anchor,
            port_names=self.port_names,
        )
        insts += transition
        ports += transition.ports

        return insts, elems, ports
    @property
    def raw_curve(self):
        IN, OUT = self.cell.ports
        return fp.g.LineBetween(IN.position, OUT.position)


if __name__ == "__main__":
    from AMFpdk_3_5_Cband.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += RIB2GRATTransition()



    fp.export_gds(library, file=gds_file)

