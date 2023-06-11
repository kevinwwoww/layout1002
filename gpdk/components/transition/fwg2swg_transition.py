from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.components.transition._fwg_transition import FWGTransition
from gpdk.technology import WG, get_technology


@dataclass(eq=False)
class FWG2SWGTransition(fp.ICurvedCellRef, fp.PCell, band="C"):
    """
    Attributes:
        length: defaults to 20, Length of transition
        wire_only_length: defaults to 5.0, Length of transition where shallow part is built up
        deep_only_width: defaults to 3.0, Core width of the waveguide at the end of shallow transition part
        fwg_type: type of FWG waveguide
        swg_type: type of SWG waveguide
        anchor: defaults to `Anchor.START`, origin of the straight(START at origin, CENTER at origin or End at origin)
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
    transition = FWG2SWGTransition(name="a", length=20, fwg_type=TECH.WG.FWG.C.WIRE, swg_type=TECH.WG.SWG.C.WIRE)
    fp.plot(transition)
    ```
    ![FWG2SWGTransition](images/fwg2swg_transition.png)
    """

    length: float = fp.PositiveFloatParam(default=20, doc="Length of transition")
    wire_only_length: float = fp.PositiveFloatParam(default=5.0, doc="Length of transition where shallow part is built up")
    deep_only_width: float = fp.PositiveFloatParam(default=3.0, doc="Core width of the waveguide at the end of shallow transition part")
    fwg_type: WG.FWG.C = fp.WaveguideTypeParam(type=WG.FWG.C)
    swg_type: WG.SWG.C = fp.WaveguideTypeParam(type=WG.SWG.C)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_fwg_type(self):
        return get_technology().WG.FWG.C.WIRE

    def _default_swg_type(self):
        return get_technology().WG.SWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        transition = FWGTransition(
            length=self.length,
            wire_only_length=self.wire_only_length,
            deep_only_width=self.deep_only_width,
            fwg_type=self.fwg_type,
            other_type=self.swg_type,
            anchor=self.anchor,
            port_names=self.port_names,
        )
        insts += transition
        ports += transition.ports

        return insts, elems, ports

    @property
    def raw_curve(self):
        IN, OUT = self.cell.ports
        return fp.g.LineBetween(IN.position, OUT.position)


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += FWG2SWGTransition()
    library += FWG2SWGTransition(name="a", length=20, fwg_type=TECH.WG.FWG.C.WIRE, swg_type=TECH.WG.SWG.C.WIRE, transform=fp.translate(0, 20))
    library += FWG2SWGTransition(name="b", length=20, deep_only_width=4, fwg_type=TECH.WG.FWG.C.WIRE, swg_type=TECH.WG.SWG.C.WIRE
                                 )
    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
