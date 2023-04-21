from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from AMFpdk_3_5_Oband.components.transition.wg_slab_to_rib import SLAB2RIBtransition
from AMFpdk_3_5_Oband.technology import WG, get_technology

@dataclass(eq=False)
class CHANNEL2SLABTransition(fp.ICurvedCellRef, fp.PCell):

    Length: float = fp.PositiveFloatParam(default=10.0, doc="Length of transition")
    Width: float = fp.PositiveFloatParam(default=0.41, doc="Length of transition")
    leftWidth: float = fp.PositiveFloatParam(default=0.3, doc="Length of transition")
    rightWidth: float = fp.PositiveFloatParam(default=5.0, doc="Length of transition")
    channel_type: fp.IWaveguideType = fp.WaveguideTypeParam(type=WG.CHANNEL.C)
    slab_type: fp.IWaveguideType = fp.WaveguideTypeParam(type=WG.SLAB.C)
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])


    def _default_channel_type(self):
        return get_technology().WG.CHANNEL.C.WIRE

    def _default_slab_type(self):
        return get_technology().WG.SLAB.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        transition = SLAB2RIBtransition(
            Length=self.Length,
            Width=self.Width,
            leftWidth=self.leftWidth,
            rightWidth=self.rightWidth,
            rib_type=self.channel_type,
            slab_type=self.slab_type,
            anchor=self.anchor,
            port_names=self.port_names
        )

        insts += transition
        ports += transition.ports

        return insts, elems, ports

    @property
    def raw_curve(self):
        IN, OUT = self.cell.ports
        return fp.g.LineBetween(IN.position, OUT.position)


if __name__ == "__main__":
    from AMFpdk_3_5_Oband.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += CHANNEL2SLABTransition()
    # library += FWG2MWGTransition(name="a", length=20, fwg_type=TECH.WG.FWG.C.WIRE, mwg_type=TECH.WG.MWG.C.WIRE, transform=fp.translate(0, 20))
    # library += FWG2MWGTransition(name="b", length=20, deep_only_width=4, fwg_type=TECH.WG.FWG.C.WIRE, mwg_type=TECH.WG.MWG.C.WIRE)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)