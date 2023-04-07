from dataclasses import dataclass

from fnpcell import all as fp
from gpdk.technology import get_technology

from step.step2.directional_coupler_bend import DirectionalCouplerBend

@dataclass(eq=False)
class MZI(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        dc = DirectionalCouplerBend(
            coupler_spacing=0.5,
            coupler_length=6,
            bend_radius=10,
            straight_after_bend=6,
            waveguide_type=TECH.WG.FWG.C.WIRE
        )
        dc1 = dc.translated(-100, 0)
        insts += dc1
        dc2 = dc.translated(100, 0)
        insts += dc2

        device = fp.create_links(
            link_type=TECH.WG.FWG.C.EXPANDED,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
            specs=[
                fp.LinkBetween(
                    dc1["op_2"],
                    dc2["op_1"],
                    waylines=[fp.until_y(-100)]
                ),
                fp.LinkBetween(
                    dc1["op_3"],
                    dc2["op_0"],
                    waylines=[fp.until_y(150),
                              fp.until_x(-50),
                              fp.until_y(100),
                              fp.until_x(50),
                              fp.until_y(150)]
                ),
            ],
        )
        insts += device
        length = device[1].curve_length
        print(length)

        ports += dc1["op_0"].with_name("in1")
        ports += dc1["op_1"].with_name("in2")
        ports += dc2["op_2"].with_name("out1")
        ports += dc2["op_3"].with_name("out2")

        # fmt: on
        return insts, elems, ports

if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    device = fp.Library()

    TECH = get_technology()

    # =============================================================
    # fmt: off

    device += MZI()

    fp.export_gds(device, file=gds_file)
    fp.plot(device)




