from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk.components.splitter.y_splitter import YSplitter
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class YCombiner(fp.PCell):
    """
    Attributes:
        bend_radius: defaults to 15, bend radius
        out_degrees: defaults to 90, Angle at which the waveguide exit the combiner
        center_waveguide_length: Length of the center waveguide
        taper_length: Length of the tapered section
        waveguide_type: type of waveguide of the combiner
        port_names: defaults to ["op_0", "op_1", "op_2"]

    Examples:
    ```python
    y_combiner = YCombiner(waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(y_combiner)
    ```
    ![YCombiner](images/y_combiner.png)
    """

    bend_radius: float = fp.PositiveFloatParam(default=15, doc="Bend radius")
    out_degrees: float = fp.DegreeParam(default=90, doc="Angle at which the waveguide exit the combiner")
    center_waveguide_length: float = fp.PositiveFloatParam(default=2.0, doc="Length of the center waveguide")
    taper_length: float = fp.PositiveFloatParam(default=0.1, doc="Length of the tapered section")
    waveguide_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=3, default=("op_0", "op_1", "op_2"))

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        # fmt: off

        splitter = YSplitter(
            bend_radius=self.bend_radius,
            out_degrees=self.out_degrees,
            center_waveguide_length=self.center_waveguide_length,
            taper_length=self.taper_length,
            waveguide_type=self.waveguide_type,
        ).h_mirrored()
        insts += splitter
        # fresh ports to right port's order in netlist
        ports += splitter["op_2"].with_name(self.port_names[0])
        ports += splitter["op_1"].with_name(self.port_names[1])
        ports += splitter["op_0"].with_name(self.port_names[2])

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += YCombiner(waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
