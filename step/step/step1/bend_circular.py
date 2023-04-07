from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology


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
        bend = BendCircular(name="s", radius=5, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(bend)
    ```
    ![BendCircular](images/bend_circular.png)

    """
    degrees: float = fp.DegreeParam(default=90, min=-180, max=180, doc="Bend angle in degrees")
    radius: float = fp.PositiveFloatParam(default=10, doc="Bend radius")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

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



if __name__ == "__main__":

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += BendCircular(name="s", radius=15, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
