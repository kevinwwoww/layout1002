import math
from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.geometry.sampler_periodic import SamplerPeriodic
from gpdk.technology import get_technology


@dataclass(eq=False)
class PnPhaseShifter(fp.PCell):
    """
    Attributes:
        ...
    Examples:
    ```python
    TECH = get_technology()
    ps = PnPhaseShifter(name="p1")
    fp.plot(ps)
    ```
    """

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        SWG = TECH.WG.SWG.C.WIRE  # .updated(core_layout_width=0.45, cladding_layout_width=3.0)

        side_wg_length = 234
        center_wg_length = 30
        x_gap = 0.25
        y_gap = 0.2
        cont_w = 0.6
        cont_h = 0.6
        m1_pin_w = 15
        m1_pin_h = 1.15
        half_m1_h = 9.0
        cladding_width = SWG.cladding_width
        side_curve = fp.g.Line(length=side_wg_length, anchor=fp.Anchor.CENTER)
        center_curve = fp.g.Line(length=center_wg_length, anchor=fp.Anchor.CENTER)
        sampler = SamplerPeriodic(period=cont_w * 5, reserved_ends=(cont_w * 5 / 2, cont_w * 5 / 2))
        cont = fp.Device(
            content=[
                fp.el.Circle(radius=0.123, layer=TECH.LAYER.CONT_DRW),
                fp.el.Rect(width=0.35, height=0.35, center=(0, 0), layer=TECH.LAYER.M1_DRW),
                fp.el.Rect(width=cont_w, height=cont_h, center=(0, 0), layer=TECH.LAYER.SIL_DRW),
            ],
            ports=[],
        )
        no_cont = fp.Device(
            content=[
                fp.el.Rect(width=cont_w, height=cont_h, center=(0, 0), layer=TECH.LAYER.SIL_DRW),
            ],
            ports=[],
        )
        cont_array = (
            cont.translated(cont_w / 2, cont_h / 2).new_array(cols=5, rows=3, col_width=cont_w, row_height=cont_h).translated(-5 * cont_w / 2, -3 * cont_h / 2)
        )
        center_cont_array = (
            no_cont.translated(cont_w / 2, cont_h / 2)
            .new_array(cols=5, rows=3, col_width=cont_w, row_height=cont_h)
            .translated(-5 * cont_w / 2, -3 * cont_h / 2)
        )

        def patch_for_wg(s: fp.SampleInfo, is_center: bool = False):
            n_cont_array = cont_array
            p_cont_array = center_cont_array if is_center else cont_array
            y_offset = cladding_width / 2 + y_gap + 3 * cont_h / 2
            array_w = cont_w * 5
            array_h = cont_h * 3
            p_plus = fp.el.Rect(width=array_w + x_gap * 2, height=array_h + y_gap * 2, center=(0, 0), layer=TECH.LAYER.PP_DRW)
            n_plus = fp.el.Rect(width=array_w + x_gap * 2, height=array_h + y_gap * 2, center=(0, 0), layer=TECH.LAYER.NP_DRW)
            p1_n1_h = array_h + y_gap + cladding_width / 2 + y_gap / 2
            p1 = fp.el.Rect(width=array_w, height=p1_n1_h, center=(0, 0), layer=TECH.LAYER.P2_DRW)
            n1 = fp.el.Rect(width=array_w, height=p1_n1_h, center=(0, 0), layer=TECH.LAYER.N2_DRW)
            p_body = fp.el.Rect(width=array_w, height=p1_n1_h - 0.525, center=(0, 0), layer=TECH.LAYER.P_DRW)
            n_body = fp.el.Rect(width=array_w, height=p1_n1_h - 0.525, center=(0, 0), layer=TECH.LAYER.N_DRW)
            m1 = fp.el.Rect(width=array_w, height=half_m1_h, center=(0, 0), layer=TECH.LAYER.M1_DRW)
            return (
                fp.Composite(
                    m1.translated(0, cladding_width / 2 + y_gap + half_m1_h / 2) if not is_center else None,
                    p_body.translated(0, p1_n1_h / 2 + 0.525 / 2),
                    p1.translated(0, p1_n1_h / 2),
                    p_plus.translated(0, y_offset),
                    p_cont_array.translated(0, y_offset),
                    n_cont_array.translated(0, y_offset),
                    n_plus.translated(0, y_offset),
                    n1.translated(0, p1_n1_h / 2),
                    n_body.translated(0, p1_n1_h / 2 - 0.525 / 2),
                    m1.translated(0, cladding_width / 2 - y_gap - half_m1_h / 2),
                )
                .rotated(radians=s.orientation)
                .translated(s.x, s.y)
            )

        # main body
        side_wg = SWG(curve=side_curve).with_patches([patch_for_wg(s) for s in sampler(side_curve)])
        center_wg = SWG(curve=center_curve).with_patches([patch_for_wg(s, True) for s in sampler(center_curve)])
        left_wg = fp.place(side_wg, "op_1", at=center_wg["op_0"])  # .translated(-side_wg_length / 2 - center_wg_length / 2, 0)
        right_wg = fp.place(side_wg, "op_0", at=center_wg["op_1"])  # .translated(side_wg_length / 2 + center_wg_length / 2, 0)
        center_metal = fp.el.Rect(width=m1_pin_w, height=half_m1_h * 2 + cladding_width + y_gap * 2, center=(0, 0), layer=TECH.LAYER.M1_DRW)
        insts += left_wg
        insts += center_wg
        insts += right_wg
        elems += center_metal

        # ports
        ports += left_wg["op_0"]
        ports += right_wg["op_1"]

        # pins
        pin_metal = fp.el.Rect(width=m1_pin_w, height=m1_pin_h, center=(0, 0), layer=TECH.LAYER.M1_DRW).translated(
            0, half_m1_h + cladding_width / 2 + y_gap + m1_pin_h / 2
        )
        elems += pin_metal
        ports += fp.Pin(
            name="ep_1", position=pin_metal.transform.translation, orientation=math.pi / 2, shape=pin_metal.shape, metal_line_type=TECH.METAL.M1.W20
        )

        pin_metal_left = pin_metal.translated(-center_wg_length - m1_pin_w / 2 - side_wg_length / 3, 0)
        elems += pin_metal_left
        ports += fp.Pin(
            name="ep_2", position=pin_metal_left.transform.translation, orientation=math.pi / 2, shape=pin_metal_left.shape, metal_line_type=TECH.METAL.M1.W20
        )

        pin_m1_right = pin_metal.translated(center_wg_length + m1_pin_w / 2 + side_wg_length / 3, 0)
        elems += pin_m1_right
        ports += fp.Pin(
            name="ep_0", position=pin_m1_right.transform.translation, orientation=math.pi / 2, shape=pin_m1_right.shape, metal_line_type=TECH.METAL.M1.W20
        )

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += PnPhaseShifter(name="p1")

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
