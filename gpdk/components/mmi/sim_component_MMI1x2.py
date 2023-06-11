from fnpcell import all as fp
import gpdk.components.all as pdk


if __name__ == "__main__":
    from pathlib import Path
    import gpdk.components.all as components

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    device = fp.Library()
    MMI = pdk.Mmi1x2()
    device += fp.Device(content=[MMI], ports=MMI.ports)
    # device += MMI
    print(MMI.ports)
    fp.export_gds(device, file=gds_file)
    fp.export_spc(device, file=gds_file.with_suffix(".spc"), components=components)
    fp.plot(device)

    ################################
    #### Start post-simulation #####
    ################################
    import sflow as sf
    import matplotlib.pyplot as plt
    import gpdk.components.all

    components = gpdk.components.all

    # Define the environment of simulation. Note that "wl_start", "wl_end", and "points_num" are necessary
    # You can also define some custom parameters, such as "T" or others
    env = dict(wl_start=1.53, wl_end=1.565, points_num=351, T=300)
    # Define the path of the netlist file
    spc_filename = Path(__file__).parent / "local" / Path(__file__).with_suffix(".spc").name
    # Export the netlist file
    fp.export_spc(device, file=spc_filename, components=components, sim_env=fp.sim.Env(**env))
    # Run simulation
    sim_result = sf.run_sim(
        input_ports=["op_0"],  # Define the port which optical signal input
        output_ports=["op_0", "op_1"],  # Define the ports which optical signal output
        env=env,  # Define the environment
        netlist_file=spc_filename,  # Define the netlist file
        # print_netlist=True  # Defines whether to print a simplified netlist information
    )
    # Get the data of each ports
    return_loss = sim_result["op_0"]
    trans_gain = sim_result["op_1"]
    # Plot figure
    plt.plot(return_loss["wl"], return_loss["te_gain"], label="Return Loss")
    plt.plot(trans_gain["wl"], trans_gain["te_gain"], label="op_1 Gain")
    plt.legend()
    plt.show()

