import math
from dataclasses import dataclass, field
from typing import Tuple
from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt
from gpdk.components.straight.straight import Straight
from gpdk.components.taper.taper_linear import TaperLinear
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(frozen=True)
class user_defined_bendfactory(fpt.IBendWaveguideFactory):
    radius_eff: float
    waveguide_type: fpt.IWaveguideType = field(repr=False, compare=False)

    def __call__(self, central_angle: float):
        from gpdk.components.bend.bend_circular import BendCircular
        radius_eff = self.radius_eff
        bend = BendCircular(degrees=math.degrees(central_angle), radius=radius_eff, waveguide_type=self.waveguide_type)
        return bend, radius_eff, ("op_0", "op_1")

TECH = get_technology()
bend_factory = user_defined_bendfactory(radius_eff=10, waveguide_type=TECH.WG.SWG.C.WIRE)

@dataclass(eq=False)
class transition(fp.PCell):


    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        straight = Straight(length=50, waveguide_type=TECH.WG.FWG.C.WIRE)

        wg1 = straight.translated(0, 0)
        wg2 = straight.rotated(degrees=90).translated(100, 25)
        wg3 = straight.rotated(degrees=90).translated(-50, 25)

        link1 = fp.create_links(
            link_type=TECH.WG.FWG.C.EXPANDED,
            # bend_factory=TECH.WG.SWG.C.WIRE.BEND_CIRCULAR,
            bend_factory=bend_factory,
            specs=[
                wg1["op_0"] >> wg2["op_1"],
                wg1["op_1"] >> wg3["op_1"],
            ],
        )

        insts += link1




        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.components import all as components
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += transition()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)

