from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology

@dataclass(eq=False)
class CircuitMzi(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        # Call component
        mmi = pdk.Mmi1x2()
        # Place components
        m1 = mmi.rotated(degrees=90).translated(-50, 0)
        insts += m1
        m2 = mmi.rotated(degrees=90).translated(50, 0)
        insts += m2
        # Create the links between ports of components
        links = fp.create_links(
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.EXPANDED.BEND_CIRCULAR,
            specs=[
                fp.LinkBetween(
                    m1["op_2"],
                    m2["op_1"],
                    target_length=200,
                ),
                fp.LinkBetween(
                    m1["op_1"],
                    m2["op_2"],
                    target_length=150
                ),
            ],
        )
        # fp.plot(fp.Library(insts))
        insts += links
        # Define the ports of the top circuit
        ports += m1["op_0"].with_name("mzi_port1")
        ports += m2["op_0"].with_name("mzi_port2")

        return insts, elems, ports

if __name__ == "__main__":
    from pathlib import Path
    # Define the path of the gds file
    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    # call Library
    device = fp.Library()
    # Add circuit in the library
    device += CircuitMzi()
    # Export gds file
    fp.export_gds(CircuitMzi(), file=gds_file)
    # Plot a figure of the circuit
    fp.plot(device)

    ################################
    #### Start post-simulation #####
    ################################
    import sflow as sf
    import matplotlib.pyplot as plt
    import gpdk.components.all

    components = gpdk.components.all

    # Define the enviroment of simulation. Note that "wl_start", "wl_end", and "points_num" are necessary.
    # You can also define some custom parameters, such as "T" or others.
    env = dict(wl_start=1.53, wl_end=1.565, points_num=351, T=300)
    # Define the path of the netlist file
    spc_filename = Path(__file__).parent / "local" / Path(__file__).with_suffix(".spc").name
    # Export the netlist file
    fp.export_spc(device, file=spc_filename, components=components, sim_env=fp.sim.Env(**env))
    
    # Run simulation
    sim_result = sf.run_sim(
        input_ports=["mzi_port1"],  # Define the port which optical signal input
        output_ports=["mzi_port1", "mzi_port2"],  # Define the ports which optical signal output
        env=env,  # Define the environment
        netlist_file=spc_filename,  # Define the netlist file
        is_print_netlist=True  # Defines whether to print a simplified netlist information
    )
    # Get the data of each ports
    return_loss = sim_result["mzi_port1"]
    trans_gain = sim_result["mzi_port2"]
    # Plot figure

    plt.plot(return_loss["wl"], return_loss["te_gain"], label="Return Loss")
    plt.plot(trans_gain["wl"], trans_gain["te_gain"], label="Gain")
    plt.legend()
    plt.show()




##

