from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk.components.splitter.y_splitter import YSplitter
from AMFpdk.technology import get_technology
from AMFpdk.technology.interfaces import CoreWaveguideType

@dataclass(eq=False)
class YCombiner(fp.PCell):
    bend_radius: float = fp.PositiveFloatParam(default=15, doc="Bend Radius")
    out_degrees: float = fp.DegreeParam(default=90, doc="Angle at which the waveguide exit the combiner")
    center_waveguide_width: float = fp.PositiveFloatParam(default=2.0, doc="Length of the center waveguide")
    taper_length: float = fp.PositiveFloatParam(default=0.1, doc="Length of the tapered section")
    waveguide_type: CoreWaveguideType = fp.WaveguideTypeParam(type=CoreWaveguideType)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=3, default=("op_1", "op_2", "op_3"))

    def _default_waveguide_type(self):
        return get_technology().WG.CHANNEL.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()

        splitter = YSplitter(
            bend_radius=self.bend_radius,
            out_degrees=self.out_degrees,
            center_waveguide_length=self.center_waveguide_width,
            taper_length=self.taper_length,
            waveguide_type=self.waveguide_type,
        ).h_mirrored()
        insts += splitter

        ports += splitter["op_2"].with_name(self.port_names[0])
        ports += splitter["op_1"].with_name(self.port_names[1])
        ports += splitter["op_0"].with_name(self.port_names[2])

        return insts, elems, ports

if __name__ =="__main__":
    from AMFpdk.util.path import local_output_file
    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += YCombiner()

    fp.export_gds(library,file=gds_file)
    fp.plot(library)