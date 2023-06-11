from dataclasses import dataclass
from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk import all as pdk


@dataclass(eq=False)
class ExampleJointsLinked(fp.PCell):
    dist: float = 1000

    def build(self):
        insts, elems, ports = super().build()

        # fmt: off
        wg_type = TECH.WG.MWG.C.WIRE
        wg_type_link = TECH.WG.SWG.C.WIRE

        # =============== instance list & place =======================
        gc1 = pdk.GratingCoupler(waveguide_type=wg_type, transform=fp.h_mirror(x=0))
        gc2 = pdk.GratingCoupler(waveguide_type=wg_type, transform=fp.translate(self.dist, 0))
        s = pdk.Straight(length=10, waveguide_type=wg_type, port_names=["op_0", fp.Hidden("op_1")])

        device_connected = fp.Connected(
            joints=[
                gc1["op_0"] <= s["op_0"],
            ],
            ports=[
                s["op_1"]
            ]
        )

        insts += device_connected.translated(0, self.dist+200)

        device_link = fp.Linked(
            link_type=wg_type_link,
            bend_factory=TECH.WG.MWG.C.WIRE.BEND_EULER,
            links=[
                gc1["op_0"] >> gc2["op_0"],
            ],
            ports=[
                gc1["op_0"].with_name("op_0"),
                gc2["op_0"].with_name("op_1"),
            ],
        )

        insts += device_link.translated(self.dist+200, 0)
        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += ExampleJointsLinked()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
