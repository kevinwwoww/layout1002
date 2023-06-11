import math
from dataclasses import dataclass

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(frozen=True)
class CircularBendFactory(fpt.IBendWaveguideFactory):
    radius_eff: float

    def __call__(self, central_angle: float):
        from gpdk.components.bend.bend_circular import BendCircular, BendCircular90

        TECH = get_technology()

        radius_eff = self.radius_eff
        degrees = math.degrees(central_angle)
        if fp.is_close(abs(degrees), 90):
            bend = BendCircular90(radius=radius_eff)
            if degrees < 0:
                bend = bend.v_mirrored()
        else:
            bend = BendCircular(degrees=degrees, radius=radius_eff, waveguide_type=TECH.WG.FWG.C.WIRE)
        return bend, radius_eff, ("op_0", "op_1")


@dataclass(eq=False)
class CircuitMzi(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        m1 = pdk.Mmi1x2()
        m2 = pdk.Mmi1x2(transform=fp.h_mirror())

        mmi1 = m1.rotated(degrees=90).translated(-100, 0)
        mmi2 = m2.rotated(degrees=-90).translated(100, 0)

        device = fp.Linked(
            link_type=TECH.WG.FWG.C.EXPANDED,
            bend_factory=CircularBendFactory(radius_eff=10),
            links=[
                fp.LinkBetween(
                    mmi1["op_2"],
                    mmi2["op_2"],
                    target_length=400,
                ),
                fp.LinkBetween(mmi1["op_1"], mmi2["op_1"], target_length=300),
            ],
            ports=[mmi1["op_0"].with_name("mzi_in"), mmi2["op_0"].with_name("mzi_out")],
        )
        insts += device
        ports += device.ports

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.components import all as components
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================

    library += CircuitMzi()

    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.export_spc(library, file=gds_file.with_suffix(".spc"), components=components, sim_env=fp.sim.Env(wl_start=1.6, wl_end=1.8, points_num=101))
    # fp.plot(library)
