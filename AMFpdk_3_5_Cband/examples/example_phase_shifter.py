from dataclasses import dataclass
from functools import cached_property
from fnpcell import all as fp
from AMFpdk_3_5_Cband.technology import get_technology
from AMFpdk_3_5_Cband.technology.interfaces.wg import CoreWaveguideType, SlabWaveguideType
@dataclass(frozen=True)
class PnPhaseShifterTemplate:
    waveguide_type: CoreWaveguideType = fp.WaveguideTypeParam(type=CoreWaveguideType)
    TECH = get_technology()

    @cached_property
    def curve_paint(self):
        TECH = get_technology()
        x_gap = 0.25
        y_gap = 0.2
        cont_w = 0.6
        cont_h = 0.6
        half_m1_h = 9.0
        slab_width = 10
        y_offset = y_gap + 3 * cont_h / 2 + slab_width / 2
        array_h = cont_h * 3
        p1_n1_h = array_h + y_gap + y_gap / 2 + slab_width / 2
        cont = fp.Device(
            name="cont",
            content=[
                fp.el.Circle(radius=0.123, layer=TECH.LAYER.VIA1),
                fp.el.Rect(width=0.35, height=0.35, center=(0, 0), layer=TECH.LAYER.MT1),
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
                    TECH.LAYER.SLAB,
                    [
                        (0, [slab_width]),
                    ],
                    (0, 0),
                ),
                (
                    TECH.LAYER.MT1,
                    [
                        (slab_width / 2 + y_gap + half_m1_h / 2, [half_m1_h]),
                        (-slab_width / 2 - y_gap - half_m1_h / 2, [half_m1_h]),
                    ],
                    (0, 0),
                ),
                (
                    TECH.LAYER.IPD,
                    [
                        (p1_n1_h / 2 + 0.535 / 2, [p1_n1_h - 0.535]),
                    ],
                    (0, 0),
                ),
                (
                    TECH.LAYER.PIM,
                    [
                        (p1_n1_h / 2, [p1_n1_h]),
                    ],
                    (0, 0),
                ),
                (
                    TECH.LAYER.PCONT,
                    [
                        (y_offset, [array_h + y_gap * 2]),
                    ],
                    (x_gap, x_gap),
                ),
                (
                    TECH.LAYER.NCONT,
                    [
                        (-y_offset, [array_h + y_gap * 2]),
                    ],
                    (x_gap, x_gap),
                ),
                (
                    TECH.LAYER.NIM,
                    [
                        (-p1_n1_h / 2, [p1_n1_h]),
                    ],
                    (0, 0),
                ),
                (
                    TECH.LAYER.IND,
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
    from AMFpdk_3_5_Cband.util.path import local_output_file
    gds_file = local_output_file(__file__).with_suffix(".gds")

    library = fp.Library()
    TECH = get_technology()

    template = PnPhaseShifterTemplate(waveguide_type=TECH.WG.RIB.C.WIRE)
    ps = template(fp.g.Arc(radius=90, final_degrees=180))

    library += ps

    fp.export_gds(library, file=gds_file)