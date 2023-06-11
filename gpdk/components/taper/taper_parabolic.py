from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class TaperParabolic(fp.IWaveguideLike, fp.PCell):
    """
    Attributes:
        length: length of straight
        left_type: type of waveguide of start
        right_type: type of waveguide of end
        step: more steps means more accurate to the parabolic curve
        anchor: defaults to `Anchor.START`, origin of the straight(START at origin, CENTER at origin or End at origin)
        port_names: defaults to ["op_0", "op_1", "op_2"]

    Examples:
    ```python
    TECH = get_technology()
        swg = TECH.WG.SWG.C.WIRE.updated(core_design_width=3.8, cladding_design_width=9.6)
    taper = TaperParabolic(name="a", length=20, left_type=swg_update, right_type=TECH.WG.SWG.C.WIRE)
    fp.plot(taper)
    ```
    ![TaperParabolic](images/taper_parabolic.png)
    """

    length: float = fp.PositiveFloatParam(default=10)
    left_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    right_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    step: float = fp.PositiveFloatParam(default=1)
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
            step=self.step,
            anchor=self.anchor,
        )

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()

        assert self.left_type.is_isomorphic_to(self.right_type), "left_type must be isomorphic to right_type"

        wgt = self.left_type.tapered(taper_function=fp.TaperFunction.PARABOLIC, final_type=self.right_type)
        wg = wgt(curve=self.raw_curve).with_ports(self.port_names)

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

    library += TaperParabolic()
    swg_update = TECH.WG.SWG.C.WIRE.updated(core_design_width=3.8, cladding_design_width=9.6)
    library += TaperParabolic(name="a", length=20, left_type=swg_update, right_type=TECH.WG.SWG.C.WIRE)
    left_type = TECH.WG.SWG.C.WIRE.updated(core_design_width=0.2, cladding_design_width=8.8)
    right_type = TECH.WG.SWG.C.WIRE.updated(core_design_width=1.8, cladding_design_width=1.8)
    library += TaperParabolic(name="b", length=10, step=0.1, left_type=left_type, right_type=right_type, transform=fp.translate(0, 20))

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
