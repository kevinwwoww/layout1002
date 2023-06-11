from typing import Any, List

from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology

if __name__ == "__main__":
    insts, elems, ports = fp.InstanceSet(), fp.ElementSet(), fp.PortSet()
    TECH = get_technology()

    RingModulator = pdk.RingModulator(gap_monitor=0.45, gap=0.31, ring_radius=10, waveguide_type=TECH.WG.FWG.C.WIRE)
    EdgeCoupler = pdk.Fixed_Edge_Coupler()
    Terminator = pdk.Fixed_Terminator_TE_1550(length=10, waveguide_type=TECH.WG.FWG.C.WIRE)
    BondPad = pdk.BondPad(pad_width=75, pad_height=75)

    MOD: List[Any] = [None] * 4
    for i in range(4):
        TM1 = Terminator.h_mirrored().translated(100, 100)
        TM2 = Terminator.translated(100, 100)
        pad1 = BondPad.translated(-150, 100)
        pad2 = BondPad.translated(0, 100)
        pad3 = BondPad.translated(150, 100)
        pad4 = BondPad.translated(-50, -150)
        pad5 = BondPad.translated(50, -150)
        RM = pdk.RingModulator(gap_monitor=0.45, gap=0.31, ring_radius=10 + i * 0.025, waveguide_type=TECH.WG.FWG.C.WIRE)

        Link = fp.Linked(
            # metal_line_width=10,
            metal_min_distance=20,
            metal_line_type=TECH.METAL.MT.W10,
            links=[
                RM["ep_0"].with_orientation(degrees=-90) >> pad4["ep_0"].with_orientation(degrees=90),
                RM["ep_1"].with_orientation(degrees=-90) >> pad5["ep_0"].with_orientation(degrees=90),
                RM["ep_2"].with_orientation(degrees=180) >> pad1["ep_0"].with_orientation(degrees=-90),
                RM["ep_2"].with_orientation(degrees=0) >> pad3["ep_0"].with_orientation(degrees=-90),
                RM["ep_3"].with_orientation(degrees=90) >> pad2["ep_0"].with_orientation(degrees=-90),
            ],
            ports=[RM["op_0"], RM["op_1"], RM["op_2"], RM["op_3"]],
        )
        MOD[i] = fp.Connected(
            joints=[
                Link["op_0"] <= TM1["op_0"],
                Link["op_3"] <= TM2["op_0"],
            ],
            ports=[Link["op_1"].with_name("op_0"), Link["op_2"].with_name("op_1")],
            transform=fp.translate(i * 450, 0),
        )

    EC1 = EdgeCoupler.translated(-150, 0)
    EC2 = EdgeCoupler.translated(-150, -250)
    to = fp.Waypoint
    Q_MOD_TX = fp.Linked(
        links=[
            EC1["op_0"] >> MOD[0]["op_0"],
            MOD[0]["op_1"] >> MOD[1]["op_0"],
            MOD[1]["op_1"] >> MOD[2]["op_0"],
            MOD[2]["op_1"] >> MOD[3]["op_0"],
            # MOD[3]["op_1"] >> to(1500, -100, -90) >> EC2["op_0"],
            fp.LinkBetween(start=MOD[3]["op_1"], end=EC2["op_0"], waypoints=[to(1500, -100, -90)], linking_policy=TECH.LINKING_POLICY.DEFAULT),
        ],
        ports=[],
    )
    insts += Q_MOD_TX
    library = fp.Library()
    library += fp.Device(name="Q_MOD_TX", content=[insts, elems], ports=ports)

    from gpdk.components import all as components
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    fp.export_gds(library, file=gds_file)

    fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=components)
    # fp.plot(library)
