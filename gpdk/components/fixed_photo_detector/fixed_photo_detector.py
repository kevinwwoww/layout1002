import math
from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.components.splitter.y_splitter import YSplitter
from gpdk.components.straight.straight import Straight
from gpdk.components.taper.taper_linear import TaperLinear
from gpdk.technology import get_technology


@dataclass(eq=False)
class Fixed_Photo_Detector(fp.PCell):
    """
    Examples:
    ```python
    pd = Fixed_Photo_Detector()
    fp.plot(pd)
    ```
    ![Fixed_Photo_Detector](images/fixed_photo_detector.png)
    """

    port_names: fp.IPortOptions = fp.PortOptionsParam(count=3, default=["op_0", "ep_0", "ep_1"])

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        port_names = self.port_names
        left_type = TECH.WG.FWG.C.WIRE.updated(core_layout_width=0.5)
        right_type = TECH.WG.FWG.C.WIRE.updated(core_layout_width=1.25)
        left_taper = TaperLinear(length=50.4, left_type=left_type, right_type=right_type, anchor=fp.Anchor.START)
        insts += left_taper
        right_taper = TaperLinear(length=50, left_type=right_type, right_type=left_type, anchor=fp.Anchor.START, transform=fp.translate(71.4, 0))
        insts += right_taper
        mid_wg = Straight(length=21, waveguide_type=right_type, transform=fp.translate(50.4, 0))
        insts += mid_wg
        splitter = YSplitter(bend_radius=5, center_waveguide_length=3.1, waveguide_type=left_type, transform=fp.translate(124.6, 0))
        insts += splitter
        right_top_wg = Straight(length=2.1, waveguide_type=left_type, anchor=fp.Anchor.CENTER, transform=fp.rotate(degrees=90).translate(129.6, 6.3))
        insts += right_top_wg
        right_bottom_wg = Straight(length=2.1, waveguide_type=left_type, anchor=fp.Anchor.CENTER, transform=fp.rotate(degrees=90).translate(129.6, -6.3))
        insts += right_bottom_wg
        right_wg = Straight(length=14.7, waveguide_type=left_type, anchor=fp.Anchor.CENTER, transform=fp.rotate(degrees=90).translate(139.6, 0))
        insts += right_wg
        top_arc = left_type(curve=fp.g.EllipticalArc(radius=5, initial_degrees=0, final_degrees=180, origin=(134.6, 7.35)))
        insts += top_arc
        bottom_arc = left_type(curve=fp.g.EllipticalArc(radius=5, initial_degrees=180, final_degrees=360, origin=(134.6, -7.35)))
        insts += bottom_arc
        elems += fp.el.Rect(width=21, height=5, center=(60.9, 4.625), layer=TECH.LAYER.FWG_COR)
        elems += fp.el.Rect(width=21, height=5, center=(60.9, -4.625), layer=TECH.LAYER.FWG_COR)
        ports += left_taper["op_0"].with_name(port_names[0])

        # SWG
        s_left_type = TECH.WG.SWG.C.WIRE.updated(core_layout_width=0.5)
        s_right_type = TECH.WG.SWG.C.WIRE.updated(core_layout_width=4.25)
        s_left_taper = TaperLinear(length=25, left_type=s_left_type, right_type=s_right_type, anchor=fp.Anchor.START, transform=fp.translate(25.4, 0))
        insts += s_left_taper
        s_right_taper = TaperLinear(length=25, left_type=s_right_type, right_type=s_left_type, anchor=fp.Anchor.START, transform=fp.translate(71.4, 0))
        insts += s_right_taper
        s_mid_wg = Straight(length=21, waveguide_type=s_right_type, transform=fp.translate(50.4, 0))
        insts += s_mid_wg

        # NP
        elems += fp.el.Polygon(
            [(50.4, 0), (50.4, 2.125), (71.4, 2.125), (71.4, 0), (70.4, 0), (68.4, 0.275), (53.4, 0.275), (51.4, 0)], layer=TECH.LAYER.NP_DRW
        )
        elems += fp.el.Rect(width=21, height=1.5, center=(60.9, 1.375), layer=TECH.LAYER.NP_DRW)
        # PP
        elems += fp.el.Polygon(
            [(50.4, 0), (50.4, -2.125), (71.4, -2.125), (71.4, 0), (70.4, 0), (68.4, -0.275), (53.4, -0.275), (51.4, 0)], layer=TECH.LAYER.PP_DRW
        )
        elems += fp.el.Rect(width=21, height=1.5, center=(60.9, -1.375), layer=TECH.LAYER.PP_DRW)
        # NPP
        elems += fp.el.Rect(width=21, height=5, center=(60.9, 4.625), layer=TECH.LAYER.NPP_DRW)
        # PPP
        elems += fp.el.Rect(width=21, height=5, center=(60.9, -4.625), layer=TECH.LAYER.PPP_DRW)
        # GE
        elems += fp.el.Polygon(
            [(53.4, -0.625), (50.4, -0.1), (50.4, 0.1), (53.4, 0.625), (68.4, 0.625), (71.4, 0.1), (71.4, -0.1), (68.4, -0.625)], layer=TECH.LAYER.GE_DRW
        )
        # CONT
        elems += fp.el.Rect(width=20, height=3, center=(60.9, 4.125), layer=TECH.LAYER.CONT_DRW)
        elems += fp.el.Rect(width=20, height=3, center=(60.9, -4.125), layer=TECH.LAYER.CONT_DRW)
        # M1 Layer
        elems += fp.el.Rect(width=21, height=10, center=(60.9, 7.125), layer=TECH.LAYER.M1_DRW)
        elems += fp.el.Rect(width=21, height=10, center=(60.9, -7.125), layer=TECH.LAYER.M1_DRW)
        # VIA1 Layer
        elems += fp.el.Rect(width=18, height=2, center=(60.9, 9.635), layer=TECH.LAYER.VIA1_DRW)
        elems += fp.el.Rect(width=18, height=2, center=(60.9, -9.635), layer=TECH.LAYER.VIA1_DRW)
        # M2 Layer
        elems += fp.el.Rect(width=21, height=10, center=(60.9, 7.125), layer=TECH.LAYER.M2_DRW)
        elems += fp.el.Rect(width=21, height=10, center=(60.9, -7.125), layer=TECH.LAYER.M2_DRW)
        # VIA2 Layer
        elems += fp.el.Rect(width=18, height=2, center=(60.9, 9.635), layer=TECH.LAYER.VIA2_DRW)
        elems += fp.el.Rect(width=18, height=2, center=(60.9, -9.635), layer=TECH.LAYER.VIA2_DRW)
        # DEVICE
        elems += fp.el.Rect(width=143, height=30, center=(71.5, 0), layer=TECH.LAYER.DEVREC_NOTE)
        ports += fp.Pin(
            name=port_names[1],
            position=(60.9, 9.625),
            orientation=math.pi / 2,
            shape=fp.g.Rect(width=18, height=2, center=(0, 0)).translated(60.9, 9.625),
            metal_line_type=TECH.METAL.M1.W20,
        )  # "elecCathode"
        ports += fp.Pin(
            name=port_names[2],
            position=(60.9, -9.625),
            orientation=-math.pi / 2,
            shape=fp.g.Rect(width=18, height=2, center=(0, 0)).translated(60.9, -9.625),
            metal_line_type=TECH.METAL.M1.W20,
        )  # "elecAnode"

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += Fixed_Photo_Detector().rotated(degrees=30).translated(0, 100)
    print(Fixed_Photo_Detector().ports)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
