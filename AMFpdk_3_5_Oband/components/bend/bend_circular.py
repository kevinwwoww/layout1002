from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Tuple

from fnpcell import all as fp
from AMFpdk_3_5_Oband.technology import get_technology, WG


@dataclass(eq=False)
class Bend(fp.IWaveguideLike, fp.PCell):
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
    Width: float = fp.PositiveFloatParam(default=0.41, doc="Bend width")
    # StartAngle: float = fp.DegreeParam(default=0, min=0, max=360, doc="Bend start angle in degree")
    EndAngle: float = fp.DegreeParam(default=90, min=-180, max=180, doc="Bend start angle in degree")
    # degrees: float = fp.DegreeParam(default=90, min=-180, max=180, doc="Bend angle in degrees")
    # Channel bend ( Si Bend 5 um radius ), set by AMF process manual
    Radius: float = fp.PositiveFloatParam(default=5, doc="Bend radius")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_waveguide_type(self):
        return get_technology().WG.CHANNEL.C.WIRE.updated(wg_design_width=self.Width)

    def __post_pcell_init__(self):
        assert fp.is_nonzero(self.EndAngle)

    @cached_property
    def raw_curve(self):
        return fp.g.EllipticalArc(
            radius=self.Radius,
            # initial_degrees=self.StartAngle,
            final_degrees=self.EndAngle,
        )


    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        wg = self.waveguide_type(curve=self.raw_curve).with_ports(self.port_names)
        insts += wg
        ports += wg.ports

        return insts, elems, ports


class Bend90(Bend):
    # StartAngle: float = fp.DegreeParam(default=0, locked=True)
    EndAngle: float = fp.DegreeParam(default=90, locked=True)


if __name__ == "__main__":
    from AMFpdk_3_5_Oband.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    # library += Bend(Width=2)
    library += Bend90(Radius=20)

    # fp.export_gds(library, file=gds_file)
    fp.plot(library)
