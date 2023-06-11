from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class Fixed_Terminator_TE_1550(fp.PCell):
    """
    Attributes:
        length: length of the terminator.
        waveguide_type: type of waveguide
        anchor: defaults to `Anchor.START`

    Examples:
    ```python
    TECH = get_technology()
        tm = Fixed_Terminator_TE_1550(length=30, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(tm)
    ```
    ![Fixed_Terminator_TE_1550](images/fixed_terminator_te_1550.png)
    """

    length: float = fp.FloatParam(min=0, default=10)
    waveguide_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=1, default=["op_0"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        wgt = self.waveguide_type.tapered(core_design_width=0.06, cladding_design_width=0.16)
        wg = wgt(curve=fp.g.Line(length=self.length, anchor=self.anchor)).with_ports([self.port_names[0], None])
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

    library += Fixed_Terminator_TE_1550()
    # library += Fixed_Terminator_TE_1550(length=30, waveguide_type=TECH.WG.FWG.C.WIRE)
    # library += Fixed_Terminator_TE_1550(length=160, waveguide_type=TECH.WG.FWG.C.WIRE).translated(0, 100)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
