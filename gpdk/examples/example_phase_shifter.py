from dataclasses import dataclass
from functools import cached_property

from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk.technology.interfaces.wg import CoreCladdingWaveguideType


@dataclass(frozen=True)
class PnPhaseShifterTemplate:
    waveguide_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)

    @cached_property
    def curve_paint(self):
        x_gap = 0.25
        y_gap = 0.2
        cont_w = 0.6
        cont_h = 0.6
        # m1_pin_w = 15
        # m1_pin_h = 1.15
        half_m1_h = 9.0
        cladding_width = self.waveguide_type.cladding_width
        y_offset = cladding_width / 2 + y_gap + 3 * cont_h / 2
        array_h = cont_h * 3
        p1_n1_h = array_h + y_gap + cladding_width / 2 + y_gap / 2
        cont = fp.Device(
            name="cont",
            content=[
                fp.el.Circle(radius=0.123, layer=TECH.LAYER.CONT_DRW),
                fp.el.Rect(width=0.35, height=0.35, center=(0, 0), layer=TECH.LAYER.M1_DRW),
            ],
            ports=[],
        )
        cont_array = (
            cont.translated(cont_w / 2, cont_h / 2).new_array(cols=1, rows=3, col_width=cont_w, row_height=cont_h).translated(-1 * cont_w / 2, -3 * cont_h / 2)
        )
        return fp.el.CurvePaint.from_profile(
            [
                *self.waveguide_type.profile,
                (
                    TECH.LAYER.M1_DRW,
                    [
                        (cladding_width / 2 + y_gap + half_m1_h / 2, [half_m1_h]),
                        (-cladding_width / 2 - y_gap - half_m1_h / 2, [half_m1_h]),
                    ],
                    (0, 0),
                ),
                (
                    TECH.LAYER.P_DRW,
                    [
                        (p1_n1_h / 2 + 0.525 / 2, [p1_n1_h - 0.525]),
                    ],
                    (0, 0),
                ),
                (
                    TECH.LAYER.P2_DRW,
                    [
                        (p1_n1_h / 2, [p1_n1_h]),
                    ],
                    (0, 0),
                ),
                (
                    TECH.LAYER.PP_DRW,
                    [
                        (y_offset, [array_h + y_gap * 2]),
                    ],
                    (x_gap, x_gap),
                ),
                (
                    TECH.LAYER.SIL_DRW,
                    [
                        (y_offset, [array_h]),
                        (-y_offset, [array_h]),
                    ],
                    (0, 0),
                ),
                # p cont
                # n cont
                (
                    TECH.LAYER.NP_DRW,
                    [
                        (-y_offset, [array_h + y_gap * 2]),
                    ],
                    (x_gap, x_gap),
                ),
                (
                    TECH.LAYER.N2_DRW,
                    [
                        (-p1_n1_h / 2, [p1_n1_h]),
                    ],
                    (0, 0),
                ),
                (
                    TECH.LAYER.N_DRW,
                    [
                        (-p1_n1_h / 2 - 0.525 / 2, [p1_n1_h - 0.525]),
                    ],
                    (0, 0),
                ),
            ]
        ) + fp.el.CurvePaint.Composite(
            [
                fp.el.CurvePaint.PeriodicSampling(pattern=cont_array, period=cont_w, reserved_ends=(cont_w / 2, cont_w / 2), offset=y_offset),
                fp.el.CurvePaint.PeriodicSampling(pattern=cont_array, period=cont_w, reserved_ends=(cont_w / 2, cont_w / 2), offset=-y_offset),
            ]
        )

    def __call__(self, curve: fp.ICurve):
        return (
            self.curve_paint(curve, offset=-20, final_offset=20)
            .with_ports(*self.waveguide_type.ports(curve, offset=-20, final_offset=20))
            .new_ref()
            .with_name("pn_phase_shifter")
        )


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off
    template = PnPhaseShifterTemplate(waveguide_type=TECH.WG.SWG.C.WIRE)
    ps = template(fp.g.Arc(radius=100, final_degrees=120))
    library += ps

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
