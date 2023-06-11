from dataclasses import dataclass
from functools import cached_property, partial

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.technology.auto_vias import taper, vias2
from gpdk.technology.interfaces import CrackedMetalLineType


@fp.hash_code
@dataclass(frozen=True)
class MT2(CrackedMetalLineType):
    @fpt.classconst
    @classmethod
    def metal_stack(cls) -> fpt.MetalStack:
        TECH = get_technology()
        return TECH.METAL.metal_stack.updated(
            layers=[
                TECH.LAYER.MT_DRW,
                TECH.LAYER.M2_DRW,
            ]
        )

    @cached_property
    def profile(self):
        TECH = get_technology()
        width = self.line_width
        max_width = self.max_width
        spacing = self.spacing
        return [
            (
                TECH.LAYER.MT_DRW,
                fp.el.CurvePaint.ContinuousLayer(layer=TECH.LAYER.MT_DRW, width=width).with_cracks(max_width=max_width, spacing=spacing).offset_widths(),
                (0, 0),
            ),
            (
                TECH.LAYER.M2_DRW,
                fp.el.CurvePaint.ContinuousLayer(layer=TECH.LAYER.M2_DRW, width=width + 1).with_cracks(max_width=max_width, spacing=spacing).offset_widths(),
                (0, 0),
            ),
        ]

    @fpt.classconst
    @classmethod
    def W10(cls):
        return cls(line_width=10)

    @fpt.classconst
    @classmethod
    def W20(cls):
        return cls(line_width=20)

    @fpt.classconst
    @classmethod
    def W40(cls):
        return cls(line_width=40)

    @fpt.classconst
    @classmethod
    def W80(cls):
        return cls(line_width=80)


@dataclass(frozen=True)
class CircularBendFactory:
    radius: float = 80

    def __call__(self, central_angle: float):
        bend = fp.g.CircularBend(radius=self.radius, radians=central_angle)
        return bend, self.radius


@dataclass(eq=False)
class LinkedElec(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        rm1 = pdk.RingFilter(waveguide_type=TECH.WG.FWG.C.WIRE)
        rm2 = pdk.RingFilter(waveguide_type=TECH.WG.FWG.C.WIRE)

        rm1 = rm1.translated(-200, 100)
        rm2 = rm2.translated(200, 100)

        MT2_2 = MT2.W10.updated(line_width=2)
        auto_vias = TECH.AUTO_VIAS.DEFAULT.updated(
            [
                (TECH.METAL.MT >> MT2, vias2),
                (MT2 >> MT2, taper),
            ]
        )
        fitting_function = partial(fp.g.Path.smooth, bend_factory=CircularBendFactory(radius=10))

        to = fp.Waypoint
        device = fp.Linked(
            metal_line_type=MT2_2,
            metal_min_distance=20,
            metal_fitting_function=fitting_function,
            auto_vias=auto_vias,
            links=[
                rm1["op_3"] >> to(0, 150, -90) >> rm2["op_0"],
                rm1["ep_1"].with_orientation(degrees=-90) >> to(0, -10, -90) >> rm2["ep_0"].with_orientation(degrees=-90),
                fp.LinkBetween(
                    rm1["ep_0"].with_orientation(degrees=-90),
                    rm2["ep_1"].with_orientation(degrees=-90),
                    start_distance=40,
                    waypoints=[to(-50, -100, -90)],
                ),
            ],
            ports=[],  # [sb10["op_0"], s40["op_1"]],
        )

        insts += device

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += LinkedElec()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
