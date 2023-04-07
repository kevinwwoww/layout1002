from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology

@dataclass(eq=False)
class ExampleConnect(fp.PCell):
    dist: float = 1000

    def build(self):
        insts, elems, ports = super().build()

        wg_type = TECH.WG.SWG.C.WIRE

        gc1 = pdk.GratingCoupler(waveguide_type=wg_type, transform=fp.h_mirror(x=0))
        gc2 = pdk.GratingCoupler(waveguide_type=wg_type, transform=fp.translate(self.dist, 0))

        device_connected = fp.Connected(
            joints=[
                gc1["op_0"] <= gc2["op_0"],
            ],
            ports=[
                gc1["op_0"].with_name("op_0"),
                gc2["op_0"].with_name("op_1"),
            ]
        )

        insts += device_connected

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")

    library = fp.Library()

    TECH = get_technology()

    library += ExampleConnect(dist=0)

    fp.export_gds(library, file=gds_file)
