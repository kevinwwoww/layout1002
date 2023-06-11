from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk import all as pdk
from gpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class FourBends(fp.PCell):
    straight_length: float = fp.PositiveFloatParam(default=10, doc="straight length")
    bend_pcell: fp.IDevice = fp.DeviceParam(type=pdk.BendEuler90, port_count=2)
    waveguide_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType, doc="Waveguide_parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_bend_pcell(self):
        return pdk.BendEuler90(radius_min=50, slab_square=True, waveguide_type=self.waveguide_type)

    def _default_waveguide_type(self):
        return get_technology().WG.SWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        # fmt: off
        straight_length = self.straight_length
        bend_pcell =self.bend_pcell
        waveguide_type = self.waveguide_type
        port_names = self.port_names

        # =========== instance list, rotate and mirror ================
        wg_st1 = pdk.Straight(length=straight_length, waveguide_type=waveguide_type)
        wg_st2 = pdk.Straight(length=straight_length, waveguide_type=waveguide_type)
        wg_st3 = pdk.Straight(length=straight_length, waveguide_type=waveguide_type)
        wg_st4 = pdk.Straight(length=straight_length, waveguide_type=waveguide_type)
        wg_st5 = pdk.Straight(length=straight_length, waveguide_type=waveguide_type)
        bend = bend_pcell
        bend1 = bend.rotated(degrees=270)
        bend2 = bend.rotated(degrees=90)
        bend3 = bend.rotated(degrees=0)
        bend4 = bend.rotated(degrees=180)

        # ====================== instance place =======================
        wg_st1 = wg_st1.translated(-straight_length, 0)  # only st1 translate is effective, other set by connection
        # =============== connection with port_pair ====================
        bend_connected = fp.Connected(
            name="4bend_conn",
            joints=[
                wg_st1["op_1"] <= bend1["op_0"],
                bend1["op_1"] <= wg_st2["op_0"],
                wg_st2["op_1"] <= bend2["op_1"],
                bend2["op_0"] <= wg_st3["op_0"],
                wg_st3["op_1"] <= bend3["op_1"],
                bend3["op_0"] <= wg_st4["op_0"],
                wg_st4["op_1"] <= bend4["op_0"],
                bend4["op_1"] <= wg_st5["op_0"],
            ],
            ports=[
                wg_st1["op_0"].with_name("op_0"),
                wg_st5["op_1"].with_name("op_1"),
            ]
        )
        insts += bend_connected
        ports += bend_connected["op_0"].with_name(port_names[0])
        ports += bend_connected["op_1"].with_name(port_names[1])

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += FourBends(waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
