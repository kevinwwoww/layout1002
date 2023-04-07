import numpy as np
from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class demux_1(fp.PCell):
    FSR: float = 80.0
    lambda_center: float = 1500
    wl_offset: float = 5
    neff: float = 2.4
    ng: float = 4.0

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        FSR = self.FSR * 1e-9
        lambda_center = self.lambda_center * 1e-9
        lambda_offset = lambda_center + self.wl_offset * 1e-9
        neff = self.neff
        ng = self.ng
        neff = neff - (lambda_offset - lambda_center) * (ng - neff) / lambda_center

        base_length = 200
        delta_length = (lambda_offset ** 2 / FSR / ng) * 1e6
        Lpi = (lambda_offset / (2 * neff)) * 1e6

        print(delta_length)

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

        ports += DC1["op_0"].with_name("in1")
        ports += DC1["op_1"].with_name("in2")
        ports += DC5["op_2"].with_name("out1")
        ports += DC5["op_3"].with_name("out2")

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from pathlib import Path

    # Define the path of the gds file
    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    # call Library
    device = fp.Library()
    # Add circuit in the library
    device += demux_1()

    # Export gds file
    fp.export_gds(device, file=gds_file)
    # Plot a figure of the circuit
    fp.plot(device)

    ###############################
    ### Start post-simulation #####
    ###############################
    import sflow as sf
    import matplotlib.pyplot as plt
    import gpdk.components.all

    components = gpdk.components.all

    # Define the environment of simulation. Note that "wl_start", "wl_end", and "points_num" are necessary
    # You can also define some custom parameters, such as "T" or others
    env = dict(wl_start=1.45, wl_end=1.55, points_num=101, T=300)
    # Define the path of the netlist file
    spc_filename = Path(__file__).parent / "local" / Path(__file__).with_suffix(".spc").name
    # Export the netlist file
    fp.export_spc(device, file=spc_filename, components=components, sim_env=fp.sim.Env(**env))
    # Run simulation
    sim_result = sf.run_sim(
        input_ports=["in1"],  # Define the port which optical signal input
        output_ports=["out1", "out2"],  # Define the ports which optical signal output
        env=env,  # Define the environment
        netlist_file=spc_filename,  # Define the netlist file
        is_print_netlist=False  # Defines whether to print a simplified netlist information
    )
    # Get the data of each ports
    out1 = sim_result["out1"]
    out2 = sim_result["out2"]
    # Plot figure
    plt.plot(out1["wl"], out1["te_gain"], label="out1")
    plt.plot(out2["wl"], out2["te_gain"], label="out2")
    plt.legend()
    plt.show()
