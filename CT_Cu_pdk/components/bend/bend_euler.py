from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Tuple, Optional

from fnpcell import all as fp
from CT_Cu_pdk.technology import get_technology
from CT_Cu_pdk.technology.interfaces import CoreWaveguideType


@dataclass(eq=False)
class BendEuler(fp.IWaveguideLike, fp.PCell):
    """
       Attributes:
           degrees: central angle in degrees
           radius_min: radius minimum
           p: radio of euler spiral in whole bend, 0 < p <= 1, when p = 1, there's no cirular part in the bend
           l_max: max length of euler spiral in half bend

               choose either p or l_max

           waveguide_type: type of waveguide of the bend
           port_names: defaults to ["op_0", "op_1"]

       Examples:
       ```python
       TECH = get_technology()
           bend = BendEuler(name="e90", radius_min=10, degrees=90, waveguide_type=TECH.WG.RIB.C.WIRE)
       fp.plot(bend)
       ```
       ![BendEuler](images/bend_euler.png)
       """

    degrees: float = fp.DegreeParam(default=90, min=-180, max=180, doc="Bend angle in degrees")
    radius_eff: float = fp.PositiveFloatParam(required=False, doc="Bend radius_eff")
    radius_min: float = fp.PositiveFloatParam(required=False, doc="Bend radius_min")
    p: Optional[float] = fp.PositiveFloatParam(required=False, max=1, doc="Bend parameter")
    l_max: Optional[float] = fp.PositiveFloatParam(required=False, doc="Bend Lmax")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_radius_eff(self):
        if self.radius_min is None:
            return 10

    def _default_waveguide_type(self):
        return get_technology().WG.Strip_WG.C.WIRE

    def __post_pcell_init__(self):
        assert self.radius_eff is not None or self.radius_min is not None, "either radius_eff or radius_min must be provided"

    @cached_property
    def raw_curve(self):
        radius_min = self.radius_min
        if radius_min is None:
            radius_min = self.radius_eff
        curve = fp.g.EulerBend(radius_min=radius_min, degrees=self.degrees, p=self.p, l_max=self.l_max)
        if self.radius_min is None and not fp.is_close(curve.radius_eff, self.radius_eff):
            curve = curve.scaled(self.radius_eff / curve.radius_eff)
        return curve

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        wg = self.waveguide_type(curve=self.raw_curve).with_ports(self.port_names)
        insts += wg
        ports += wg.ports
        return insts, elems, ports


@dataclass(eq=False)
class BendEuler90(BendEuler):
    """
    Attributes:
        slab_square: bool, whether draw a square clad

        radius_min: radius minimum
        radius_eff: radius effective

            choose either radius_min(imum) or radius_eff(ective)

        p: radio of euler spiral in whole bend, 0 < p <= 1, when p = 1, there's no cirular part in the bend
        l_max: max length of euler spiral in half bend

            choose either p or l_max

        waveguide_type: type of waveguide of the bend
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
        bend = BendEuler90(name="e90c", radius_min=10, slab_square=True, waveguide_type=TECH.WG.RIB.C.WIRE)
    fp.plot(bend)
    ```
    ![BendEuler90](images/bend_euler_90.png)
    """

    degrees: float = fp.DegreeParam(default=90, min=90, max=90, locked=True, doc="Bend angle in degrees")
    waveguide_type: CoreWaveguideType = fp.WaveguideTypeParam(type=CoreWaveguideType, doc="Waveguide parameters")
    slab_square: bool = fp.BooleanParam(required=False, default=False, doc="whether draw a square clad")

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        waveguide_type = self.waveguide_type

        if self.slab_square:
            r = self.raw_curve.radius_eff
            w = r + waveguide_type.wg_width / 2
            x = w / 2
            y = (r - waveguide_type.wg_width / 2) / 2
            elems += fp.el.Rect(width=w, height=w, center=(x, y), layer=waveguide_type.wg_layer)

        return insts, elems, ports


@dataclass(eq=False)
class BendEuler90_Strip_WG_C_WIRE(BendEuler90, locked=True):
    l_max: Optional[float] = fp.PositiveFloatParam(default=5, doc="Bend Lmax")
    radius_min: float = fp.PositiveFloatParam(default=5.1, doc="Bend radius_min")
    waveguide_type: CoreWaveguideType = fp.WaveguideTypeParam(type=CoreWaveguideType, doc="Waveguide parameters")
    slab_square: bool = fp.BooleanParam(required=False, default=False, doc="whether draw a square clad")

    def _default_waveguide_type(self):
        return get_technology().WG.Strip_WG.C.WIRE




if __name__ == "__main__":
    from CT_Cu_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += BendEuler(degrees=90, radius_eff=10)
    library += BendEuler(name="s", radius_eff=15)
    library += BendEuler90(name="k", radius_eff=8)
    fp.export_gds(library, file=gds_file)
    fp.plot(library)

    print(BendEuler.port_names)
