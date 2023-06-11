from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class TaperLinear(fp.IWaveguideLike, fp.PCell):
    """
    Attributes:
        length: length of straight
        left_type: type of waveguide of start
        right_type: type of waveguide of end
        anchor: defaults to `Anchor.START`, origin of the straight(START at origin, CENTER at origin or End at origin)
        port_names: defaults to ["op_0", "op_1", "op_2"]

    Examples:
    ```python
    TECH = get_technology()
        swg = TECH.WG.SWG.C.WIRE.updated(core_design_width=3.8, cladding_design_width=9.6)
    taper = TaperLinear(name="a", length=20, left_type=swg, right_type=TECH.WG.SWG.C.WIRE)
    fp.plot(taper)
    ```
    ![TaperLinear](images/taper_linear.png)
    """

    length: float = fp.PositiveFloatParam(default=10)
    left_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    right_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.CENTER)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_left_type(self):
        return get_technology().WG.FWG.C.WIRE

    def _default_right_type(self):
        return get_technology().WG.FWG.C.EXPANDED

    @cached_property
    def raw_curve(self):
        return fp.g.Line(
            length=self.length,
            anchor=self.anchor,
        )

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        assert self.left_type.is_isomorphic_to(self.right_type), "left_type must be isomorphic to right_type"

        wgt = self.left_type.tapered(taper_function=fp.TaperFunction.LINEAR, final_type=self.right_type)
        wg = wgt(curve=self.raw_curve).with_ports(self.port_names)
        insts += wg
        ports += wg.ports
        return insts, elems, ports


if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += TaperLinear(length=20, left_type=TECH.WG.SWG.C.WIRE, right_type=TECH.WG.SWG.C.EXPANDED)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
