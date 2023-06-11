import math
from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(frozen=True)
class SCosine(fp.g.FunctionCurve):
    distance: float
    height: float
    transform: fp.Affine2D = fp.Affine2D.identity()

    def curve_function(self, t: float):
        t = fp.clamp(t, 0, 1)
        theta = math.pi + t * math.pi
        x = self.distance * t
        y = math.cos(theta) * self.height / 2
        return (x, y)

    @property
    def raw_end_orientations(self) -> Optional[Tuple[float, float]]:
        return (math.pi, 0)


@dataclass(eq=False)
class SBendCosine(fp.IWaveguideLike, fp.PCell):
    """
    Attributes:
        distance: defaults to 20
        height: defaults to 10
        min_radius: required=False
        waveguide_type: type of waveguide
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
        sbend = SBendCosine(name="f", distance=100, height=15, min_radius=15, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(sbend)
    ```
    ![SBendCosine](images/sbend_cosine.png)
    """

    distance: float = fp.PositiveFloatParam(default=20)
    height: float = fp.FloatParam(default=10, invalid=[0])
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=("op_0", "op_1"))

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    @cached_property
    def raw_curve(self):
        return SCosine(distance=self.distance, height=self.height)

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        wg = self.waveguide_type(curve=self.raw_curve).with_ports(self.port_names)
        insts += wg
        ports += wg.ports
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += SBendCosine()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    #  fp.plot(library)
