from fnpcell import all as fp
import gpdk.components.all as pdk
from dataclasses import dataclass
from typing import Tuple
from gpdk.components.straight.straight import Straight
from gpdk.technology import get_technology

@dataclass(eq=False)
class straight_sim(fp.PCell):

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        straight1 = Straight(length=1000)
        straight2 = Straight(length=1000).translated(2500, 500)

        link = fp.Linked(
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER,
            links=[
                straight1["op_1"] >> straight2["op_0"]
            ],
            ports=[
                straight1["op_0"].with_name("op_0"),
                straight2["op_1"].with_name("op_1")

            ]

        )

        # link = fp.create_links(
        #     link_type=TECH.WG.FWG.C.WIRE,
        #     bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER,
        #     specs=[
        #         fp.LinkBetween(
        #             start=straight1["op_1"],
        #             end=straight2["op_0"],
        #         )
        #     ]
        #
        # )

        insts += straight1, link, straight2
        ports += straight1["op_0"].with_name("op_0")
        ports += straight2["op_1"].with_name("op_1")

        return insts, elems, ports




if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    device = fp.Library()
    device += straight_sim()
    # print(MMI.ports)
    fp.export_gds(device, file=gds_file)


    fp.plot(device)

    import sflow as sf
    import matplotlib.pyplot as plt
    import gpdk.components.all

    components = gpdk.components.all

    # Define the environment of simulation. Note that "wl_start", "wl_end", and "points_num" are necessary
    # You can also define some custom parameters, such as "T" or others
    env = dict(wl_start=1.53, wl_end=1.565, points_num=3510)
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
    # plt.plot(return_loss["wl"], return_loss["te_gain"], label="Return Loss")
    plt.plot(trans_gain["wl"], trans_gain["te_gain"], label="op_1 Gain")
    plt.legend()
    plt.show()
