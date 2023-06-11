from dataclasses import dataclass
from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class EllipticalRings(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        # fmt: off
        TECH = get_technology()

        elems += fp.el.EllipticalRing(outer_radius=(10,4), inner_radius=(5,2), initial_degrees=(60, 30), final_degrees=(120, 150), layer=TECH.LAYER.M1_DRW)
        elems += fp.el.Ring(outer_radius=4, inner_radius=2, initial_degrees=(60, 30), final_degrees=(120, 150), layer=TECH.LAYER.M2_DRW, origin=(30, 0))
        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += EllipticalRings()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
