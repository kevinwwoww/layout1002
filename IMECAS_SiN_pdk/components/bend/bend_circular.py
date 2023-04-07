from dataclasses import dataclass
from functools import cached_property
from typing import Tuple
from fnpcell import all as fp
from IMECAS_SiN_pdk.technology import get_technology



@dataclass(eq=False)
class Bend(fp.IWaveguideLike, fp.PCell):
    degrees: float = fp.DegreeParam(default=90, min=-180, max=180, doc="Bend angle in degrees")
    radius: float = fp.PositiveFloatParam(default=10, doc="Bend radius")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_waveguide_type(self):
        return get_technology().WG.Channel.C.WIRE

    def __post_pcell_init__(self):
        assert fp.is_nonzero(self.degrees)

    @cached_property
    def raw_curve(self):
        return fp.g.EllipticalArc(
            radius=self.radius,
            final_degrees=self.degrees,
        )

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        wg = self.waveguide_type(curve=self.raw_curve).with_ports(self.port_names)
        insts += wg
        ports += wg.ports
        return insts, elems, ports


@dataclass(eq=False)
class Bend_C(Bend, locked=True):
    degree: float = fp.DegreeParam(default=90, locked=True)
    radius: float = fp.PositiveFloatParam(default=100, doc="Bend radius")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(locked=True)


@dataclass(eq=False)
class Bend_O(Bend, locked=True):
    degree: float = fp.DegreeParam(default=90, locked=True)
    radius: float = fp.PositiveFloatParam(default=100, doc="Bend radius")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()

    def _default_waveguide_type(self):
        return get_technology().WG.Channel.O.WIRE


if __name__ == "__main__":
    from IMECAS_SiN_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    # library += Bend()
    # library += Bend_C()
    library += Bend_O()

    # fmt: on
    # =============================================================
    # fp.export_gds(library, file=gds_file)
    fp.plot(library)
