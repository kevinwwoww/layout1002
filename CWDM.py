import numpy as np
from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from sim_circuit_demux import demux_1, demux_2


@dataclass(eq=False)
class cwdm(fp.PCell):

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        gap = 100

        demux1 = demux_1()
        insts += demux1
        demux2 = demux_2().translated(200 + gap, 200)
        insts += demux2
        demux3 = demux_1().translated(200 + gap, -200)
        insts += demux3
        demux4 = demux_1().translated(400 + 2 * gap, 400)
        insts += demux4
        demux5 = demux_1().translated(400 + 2 * gap, -400)
        insts += demux5
        demux6 = demux_2().translated(600 + 3 * gap, 600)
        insts += demux6
        demux7 = demux_1().translated(600 + 3 * gap, 300)
        insts += demux7
        demux8 = demux_2().translated(600 + 3 * gap, -300)
        insts += demux8
        demux9 = demux_1().translated(600 + 3 * gap, -600)
        insts += demux9

        CWDM = fp.create_links(
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
            specs=[
                fp.LinkBetween(
                    demux1["out2"],
                    demux2["in2"]
                ),
                fp.LinkBetween(
                    demux1["out1"],
                    demux3["in1"]
                ),
                fp.LinkBetween(
                    demux2["out1"],
                    demux4["in1"]
                ),
                fp.LinkBetween(
                    demux3["out1"],
                    demux5["in1"]
                ),
                fp.LinkBetween(
                    demux4["out2"],
                    demux6["in2"]
                ),
                fp.LinkBetween(
                    demux4["out1"],
                    demux7["in1"]
                ),
                fp.LinkBetween(
                    demux5["out2"],
                    demux8["in2"]
                ),
                fp.LinkBetween(
                    demux5["out1"],
                    demux9["in1"]
                ),
            ],
        )
        insts += CWDM

        return insts, elems, ports


if __name__ == "__main__":
    from pathlib import Path

    # Define the path of the gds file
    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    # call Library
    library = fp.Library()
    # Add circuit in the library
    library += cwdm()
    # Export gds file
    fp.export_gds(library, file=gds_file)
