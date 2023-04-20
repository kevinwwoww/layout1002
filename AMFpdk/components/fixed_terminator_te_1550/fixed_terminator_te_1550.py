from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk.technology import get_technology
from AMFpdk.technology.interfaces import CoreWaveguideType

@dataclass(eq=False)
class Fixed_Terminator_TE_1550(fp.PCell):

    length: float = fp.FloatParam(min=0, default=10)
    waveguide_type: CoreWaveguideType = fp.WaveguideTypeParam(type=CoreWaveguideType)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=1, default=["op_0"])

    def _default_waveguide_type(self):
        return get_technology().WG.CHANNEL.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        wgt = self.waveguide_type.tapered(wg_design_width=0.06)
        wg = wgt(curve=fp.g.Line(length=self.length, anchor=self.anchor)).with_ports([self.port_names[0], None])
        insts += wg
        ports += wg.ports

        return insts, elems, ports



if __name__ =="__main__":
    from AMFpdk.util.path import local_output_file
    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += Fixed_Terminator_TE_1550()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
