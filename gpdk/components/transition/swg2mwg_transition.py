from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.components.straight.straight import Straight
from gpdk.components.transition.fwg2mwg_transition import FWG2MWGTransition
from gpdk.components.transition.fwg2swg_transition import FWG2SWGTransition
from gpdk.technology import WG, get_technology


@dataclass(eq=False)
class SWG2MWGTransition(fp.ICurvedCellRef, fp.PCell):
    """
    Attributes:
        swg_length: defaults to 20, Length of transition
        swg_wire_only_length: defaults to 5.0, Length of transition where shallow part is built up
        swg_deep_only_width: defaults to 3.0, Core width of the waveguide at the end of shallow transition part
        swg_type: type of SWG waveguide
        mwg_length: defaults to 20, Length of transition
        mwg_wire_only_length: defaults to 5.0, Length of transition where shallow part is built up
        mwg_deep_only_width: defaults to 3.0, Core width of the waveguide at the end of shallow transition part
        mwg_type: type of MWG waveguide
        anchor: defaults to `Anchor.START`, origin of the straight(START at origin, CENTER at origin or End at origin)
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
    transition = SWG2MWGTransition(name="a", swg_type=TECH.WG.SWG.C.WIRE, mwg_type=TECH.WG.MWG.C.WIRE)
    fp.plot(transition)
    ```
    ![SWG2MWGTransition](images/swg2mwg_transition.png)
    """

    swg_length: float = fp.PositiveFloatParam(default=20)
    swg_wire_only_length: float = fp.PositiveFloatParam(default=5.0)
    swg_deep_only_width: float = fp.PositiveFloatParam(default=3.0)
    swg_type: WG.SWG.C = fp.WaveguideTypeParam(type=WG.SWG.C)
    mwg_length: float = fp.PositiveFloatParam(default=20)
    mwg_wire_only_length: float = fp.PositiveFloatParam(default=5.0)
    mwg_deep_only_width: float = fp.PositiveFloatParam(default=3.0)
    mwg_type: WG.MWG.C = fp.WaveguideTypeParam(type=WG.MWG.C)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_swg_type(self):
        return get_technology().WG.SWG.C.WIRE

    def _default_mwg_type(self):
        return get_technology().WG.MWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off

        swg_length = self.swg_length
        swg_wire_only_length = self.swg_wire_only_length
        swg_deep_only_width = self.swg_deep_only_width
        swg_type = self.swg_type
        mwg_length =self.mwg_length
        mwg_wire_only_length = self.mwg_wire_only_length
        mwg_deep_only_width = self.mwg_deep_only_width
        mwg_type = self.mwg_type
        anchor = self.anchor
        port_names = self.port_names
        straight_length = 5
        total_length = swg_length + straight_length + mwg_length
        tx = 0

        if anchor == fp.Anchor.END:
            tx = -total_length
        elif anchor == fp.Anchor.CENTER:
            tx = -total_length / 2
        transform = fp.translate(tx, 0)
        fwg2swg = FWG2SWGTransition(
            name="swg",
            length=swg_length,
            wire_only_length=swg_wire_only_length,
            deep_only_width=swg_deep_only_width,
            fwg_type=TECH.WG.FWG.C.WIRE,
            swg_type=swg_type,
            transform=fp.rotate(degrees=180).translate(-straight_length / 2, 0) @ transform,
        )
        insts += fwg2swg
        ports += fwg2swg["op_1"].with_name(port_names[0])
        straight = Straight(
            name="straight",
            length=straight_length,
            waveguide_type=TECH.WG.FWG.C.WIRE,
            anchor=fp.Anchor.CENTER,
            transform=transform,
        )
        insts += straight
        fwg2mwg = FWG2MWGTransition(
            name="mwg",
            length=mwg_length,
            wire_only_length=mwg_wire_only_length,
            deep_only_width=mwg_deep_only_width,
            fwg_type=TECH.WG.FWG.C.WIRE,
            mwg_type=mwg_type,
            transform=fp.translate(straight_length / 2, 0) @ transform,
        )
        insts += fwg2mwg
        ports += fwg2mwg["op_1"].with_name(port_names[1])

        # fmt: on
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

    library += SWG2MWGTransition()
    library += SWG2MWGTransition(name="a", swg_type=TECH.WG.SWG.C.WIRE, mwg_type=TECH.WG.MWG.C.WIRE, transform=fp.translate(0, 20))

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
