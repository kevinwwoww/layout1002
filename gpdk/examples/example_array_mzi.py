import math
from dataclasses import dataclass
from typing import Mapping, cast

from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class Linked(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off

        dc1 = pdk.DirectionalCouplerBend(coupler_length=10, coupler_spacing=1.2, bend_radius=10,
                                          waveguide_type=TECH.WG.FWG.C.WIRE)
        dc2 = pdk.DirectionalCouplerBend(coupler_length=10, coupler_spacing=1.2, bend_radius=10,
                                          waveguide_type=TECH.WG.FWG.C.WIRE)
        om = pdk.PnPhaseShifter(wg_length=80, waveguide_type=TECH.WG.FWG.C.WIRE)
        wg = pdk.Straight(length=40, waveguide_type=TECH.WG.FWG.C.WIRE)

        dc1 = dc1.translated(-100, 0)
        dc2 = dc2.translated(100, 0)
        om = om.translated(-40, 50)
        wg = wg.translated(-20, -50)


        mzi = fp.Linked(
            link_type=TECH.WG.FWG.C.EXPANDED,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER,
            links=[
                dc1["op_2"] >> wg["op_0"],
                wg["op_1"] >> dc2["op_1"],
                dc1["op_3"] >> om["op_0"],
                om["op_1"] >> dc2["op_0"],
            ],
            ports=[
                dc1["op_0"].with_name("op_0"),
                dc1["op_1"].with_name("op_1"),
                dc2["op_2"].with_name("op_2"),
                dc2["op_3"].with_name("op_3"),
            ],
        )
        rows = 6
        cols = 7
        period_x = 600
        period_y = 200

        for i in range(rows):
            for j in range(cols):
                if (i % 2) == 0:
                    mzi_array = mzi.translated(period_x * j, period_y / 2 * math.sqrt(3) * i)
                else:
                    mzi_array = mzi.translated(period_x * j + period_x / 2, period_y / 2 * math.sqrt(3) * i)
                insts += mzi_array, f"{i},{j}"

        mapping = cast(Mapping[str, fp.ICellRef], insts)
        for i in range(rows):
            for j in range(cols):
                it = mapping[f"{i},{j}"]
                n = i % 2
                if n == 0:
                    if i == 0:
                        if j != cols - 1:
                            link = fp.LinkBetween(start=it["op_2"], end=mapping[f"{i},{j + 1}"]["op_1"])
                            insts += link
                    if i != rows-1:
                        link = fp.LinkBetween(start=it["op_3"], end=mapping[f"{i+1},{j}"]["op_1"])
                        insts += link
                        if j != 0:
                            link = fp.LinkBetween(start=it["op_0"], end=mapping[f"{i+1},{j-1}"]["op_2"])
                            insts += link
                    else:
                        if j != cols-1:
                            link = fp.LinkBetween(start=it["op_3"], end=mapping[f"{i},{j+1}"]["op_0"])
                            insts += link
                else:
                    if i != rows-1:
                        link = fp.LinkBetween(start=it["op_0"], end=mapping[f"{i+1},{j}"]["op_2"])
                        insts += link
                        if j != cols-1:
                            link = fp.LinkBetween(start=it["op_3"], end=mapping[f"{i+1},{j+1}"]["op_1"])
                            insts += link

                    if i == rows - 1:
                        if j != cols - 1:
                            link = fp.LinkBetween(start=it["op_3"], end=mapping[f"{i},{j + 1}"]["op_0"])
                            insts += link

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += Linked()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
