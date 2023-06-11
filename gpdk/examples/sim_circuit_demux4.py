import math

import numpy as np

from dataclasses import dataclass

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt
from gpdk import all as pdk
from gpdk.technology import PCell, get_technology

@dataclass(eq=False)
class demux(fp.PCell):
    FSR: float = 40 * 1e-9,
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        FSR = self.FSR
        lambda_center = 1.310 * 1e-6
        neff = 2.4
        ng = 4.0

        base_length = 200
        delta_length = (lambda_center**2 / FSR / ng) * 1e6
        Lpi = (lambda_center / (2 * neff)) * 1e6

        DC_050 = pdk.DC_050()
        DC_025 = pdk.DC_025()
        DC_013 = pdk.DC_013()
        DC_012 = pdk.DC_012()

        DC1 = DC_050.translated(-100, 0)
        insts += DC1
        DC2 = DC_013.translated(-50, 0)
        insts += DC2
        DC3 = DC_012.translated(0, 0)
        insts += DC3
        DC4 = DC_050.translated(50, 0)
        insts += DC4
        DC5 = DC_025.translated(100, 0)
        insts += DC5

        device = fp.create_links(
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
            specs=[
                fp.LinkBetween(
                    DC1["op_2"],
                    DC2["op_1"],
                    target_length=base_length,
                ),
                fp.LinkBetween(
                    DC1["op_3"],
                    DC2["op_0"],
                    target_length=base_length + delta_length
                ),
                fp.LinkBetween(
                    DC2["op_2"],
                    DC3["op_1"],
                    target_length=base_length
                ),
                fp.LinkBetween(
                    DC2["op_3"],
                    DC3["op_0"],
                    target_length=base_length + 2 * delta_length
                ),
                fp.LinkBetween(
                    DC3["op_2"],
                    DC4["op_1"],
                    target_length=base_length + 2 * delta_length + Lpi
                ),
                fp.LinkBetween(
                    DC3["op_3"],
                    DC4["op_0"],
                    target_length=base_length
                ),
                fp.LinkBetween(
                    DC4["op_2"],
                    DC5["op_1"],
                    target_length=base_length + 2 * delta_length
                ),
                fp.LinkBetween(
                    DC4["op_3"],
                    DC5["op_0"],
                    target_length=base_length
                ),
            ],
        )
        insts += device
        ports += DC1["op_0"].with_name("op_0")
        ports += DC1["op_1"].with_name("op_1")
        ports += DC5["op_2"].with_name("op_2")
        ports += DC5["op_3"].with_name("op_3")

        # fmt: on
        return insts, elems, ports

@dataclass(eq=False)
class demux4(PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        demux40 = demux(FSR=40 * 1e-9)
        demux80 = demux(FSR=80 * 1e-9)

        D1 = demux40.translated(0, 0)
        insts += D1
        D2 = demux40.translated(300, -200)
        insts += D2
        D3 = demux40.v_mirrored().translated(300, 200)
        insts += D3
        D4 = demux80.translated(600, -400)
        insts += D4
        D5 = demux80.translated(900, -550)
        insts += D5
        D6 = demux80.v_mirrored().translated(900, -250)
        insts += D6
        D7 = demux80.translated(600, 400)
        insts += D7
        D8 = demux80.translated(900, 250)
        insts += D8
        D9 = demux80.v_mirrored().translated(900, 550)
        insts += D9
        device = fp.create_links(
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
            specs=[
                fp.LinkBetween(
                    start=D1["op_2"],
                    end=D2["op_0"],
                ),
                fp.LinkBetween(
                    start=D1["op_3"],
                    end=D3["op_0"],
                ),
                fp.LinkBetween(
                    start=D2["op_2"],
                    end=D4["op_0"],
                ),
                fp.LinkBetween(
                    start=D3["op_3"],
                    end=D7["op_0"],
                ),
                fp.LinkBetween(
                    start=D4["op_2"],
                    end=D5["op_0"],
                ),
                fp.LinkBetween(
                    start=D4["op_3"],
                    end=D6["op_0"],
                ),
                fp.LinkBetween(
                    start=D7["op_2"],
                    end=D8["op_0"],
                ),
                fp.LinkBetween(
                    start=D7["op_3"],
                    end=D9["op_0"],
                ),

            ],
        )
        insts += device

        ports += D1["op_0"].with_name("p_0")
        ports += D5["op_2"].with_name("p_1")
        ports += D5["op_3"].with_name("p_2")
        ports += D6["op_3"].with_name("p_3")
        ports += D6["op_2"].with_name("p_4")
        ports += D8["op_2"].with_name("p_5")
        ports += D8["op_3"].with_name("p_6")
        ports += D9["op_3"].with_name("p_7")
        ports += D9["op_2"].with_name("p_8")

        # fmt: on
        return insts, elems, ports
if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    spc_filename = Path(__file__).parent / "local" / Path(__file__).with_suffix(".spc").name
    device = fp.Library()

    TECH = get_technology()

    import gpdk.components.all
    components = gpdk.components.all

    # =============================================================
    # fmt: off

    device += demux4()

    fp.export_gds(device, file=gds_file)

    fp.plot(device)
    #
    # start execution simulation
    # import sflow as sf
    # import matplotlib.pyplot as plt
    #
    # components = gpdk.components.all
    #
    # env = sf.PsimEnvironment(wl_start=1.26, wl_end=1.36, points_num=100, source_power=0, input_ports=["p_0"],
    #                          output_ports=["p_1", "p_2", "p_3", "p_4", "p_5", "p_6", "p_7", "p_8"])
    # fp.export_spc(device, file=spc_filename, components=components, sim_env=fp.sim.Env(wavelength=env.wl_range))
    #
    # sim_result = sf.run_sim(spc_filename, env, is_print_netlist=True)
    #
    # data_1 = sim_result["p_1"]
    # data_2 = sim_result["p_2"]
    # data_3 = sim_result["p_3"]
    # data_4 = sim_result["p_4"]
    # data_5 = sim_result["p_5"]
    # data_6 = sim_result["p_6"]
    # data_7 = sim_result["p_7"]
    # data_8 = sim_result["p_8"]
    # plt.plot(data_1["wl"], data_1["te_gain"], label="trans_p1")
    # plt.plot(data_2["wl"], data_2["te_gain"], label="trans_p2")
    # plt.plot(data_3["wl"], data_3["te_gain"], label="trans_p3")
    # plt.plot(data_4["wl"], data_4["te_gain"], label="trans_p4")
    # plt.plot(data_5["wl"], data_5["te_gain"], label="trans_p5")
    # plt.plot(data_6["wl"], data_6["te_gain"], label="trans_p6")
    # plt.plot(data_7["wl"], data_7["te_gain"], label="trans_p7")
    # plt.plot(data_8["wl"], data_8["te_gain"], label="trans_p8")
    #
    # plt.legend()
    # plt.show()



