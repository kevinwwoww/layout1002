from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Tuple

from fnpcell import all as fp
from CT_Cu_pdk.technology import get_technology


@dataclass(eq=False)
class BendCircular(fp.IWaveguideLike, fp.PCell):
    """
    Attributes:
        degrees: central angle of the bend, in degrees
        radius: raidus of the bend
        waveguide_type: type of waveguide of the bend
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
        bend = BendCircular(name="s", radius=5, waveguide_type=TECH.WG.RIB.C.WIRE)
    fp.plot(bend)
    ```
    ![BendCircular](images/bend_circular.png)
    """

    degrees: float = fp.DegreeParam(default=90, min=-180, max=180, doc="Bend angle in degrees")
    radius: float = fp.PositiveFloatParam(default=5, doc="Bend radius")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_waveguide_type(self):
        return get_technology().WG.Strip_WG.C.WIRE

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
class BendCircular90(BendCircular):
    degrees: float = fp.DegreeParam(default=90, locked=True)
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(locked=True)


@dataclass(eq=False)
class BendCircular90_Strip_WG_C_WIRE(BendCircular90, locked=True):
    radius: float = fp.PositiveFloatParam(default=5, doc="Bend radius")


@dataclass(eq=False)
class BendCircular90_Rib_WG_C_WIRE(BendCircular):
    degrees: float = fp.DegreeParam(default=90, locked=True)
    radius: float = fp.PositiveFloatParam(default=5, doc="Bend radius")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()

    def _default_waveguide_type(self):
        return get_technology().WG.Rib_WG.C.WIRE


if __name__ == "__main__":
    from CT_Cu_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    library += BendCircular90_Rib_WG_C_WIRE()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
