# import math
# from dataclasses import dataclass
# from typing import Tuple
# from fnpcell import all as fp
# from AMFpdk.components.splitter.y_splitter import YSplitter
# from AMFpdk.components.straight.straight import Straight
# from AMFpdk.components.taper.taper_linear import TaperLinear
# from AMFpdk.technology import get_technology
#
# @dataclass(eq=False)
# class Fixed_Photo_Detector(fp.PCell):
#     port_names: fp.IPortOptions = fp.PortOptionsParam(count=3, default=["op_0", "ep_0", "ep_1"])
#
#     def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
#         insts, elems, ports = super().build()
#         TECH = get_technology()
#
#         port_names = self.port_names
#
#         left_type = TECH.WG.RIB.C.WIRE.updated(wg_layout_width=0.5)
#         right_type = TECH.WG.RIB.C.WIRE.updated(wg_layout_width=1.25)
#
#         left_taper = TaperLinear(length=50.4, left_type=left_type, right_type=right_type, anchor=fp.Anchor.START)
#         insts += left_taper
#         right_taper = TaperLinear(length=50, left_type=right_type, right_type=left_type, anchor=fp.Anchor.START, transform=fp.translate(71.4, 0))
#         insts += right_taper
#
#         mid_wg = Straight(length=21, waveguide_type=right_type, transform=fp.translate(50.4, 0))
#         insts += mid_wg
#
#         splitter= YSplitter(bend_radius=5, center_waveguide_length=3.1, waveguide_type=left_type, transform=fp.translate(124.6, 0))
#         insts += splitter
#
#         right_top_wg = Straight(length=2.1, waveguide_type=left_type, anchor=fp.Anchor.CENTER, transform=fp.rotate(degrees=90).translate(129.6, 6.3))
#         insts += right_top_wg
#         right_bottom_wg = Straight(length=2.1, waveguide_type=left_type, anchor=fp.Anchor.CENTER, transform=fp.rotate(degrees=90).translate(129.6, -6.3))
#         insts += right_bottom_wg
#
#         right_wg = Straight(length=14.7, waveguide_type=left_type, anchor=fp.Anchor.CENTER, transform=fp.rotate(degrees=90).translate(139.6, 0))
#         insts += right_wg
#
#         top_arc = left_type(curve=fp.g.EllipticalArc(radius=5, initial_degrees=0, final_degrees=180, origin=(134.6, 7.35)))
#         insts += top_arc
#         bottom_arc = left_type(curve=fp.g.EllipticalArc(radius=5, initial_degrees=180, final_degrees=360, origin=(134.6, -7.35)))
#         insts += bottom_arc
#
#         elems += fp.el.Rect(width=21, height=5, center=(60.9, 4.625), layer=TECH.LAYER.RIB)
#         elems += fp.el.Rect(width=21, height=5, center=(60.9, -4.625), layer=TECH.LAYER.RIB)
#
#         ports += left_taper["op_0"].with_name(port_names[0])
#
#         shallow etch
        # s_left_type = TECH.WG.SLAB.C.WIRE.updated(wg_layout_width=0.5)
        # s_right_type = TECH.WG.SLAB.C.WIRE.updated(wg_layout_width=4.25)
        #
        # s_left_taper = TaperLinear(length=25, left_type=s_left_type, right_type=s_right_type, anchor=fp.Anchor.START, transform=fp.translate(25.4, 0))
        # insts += s_left_taper
        # s_right_taper = TaperLinear(length=25, left_type=s_right_type, right_type=s_left_type, anchor=fp.Anchor.START, transform=fp.translate(71.4, 0))
        # insts += s_right_taper
        #
        # s_mid_wg = Straight(length=21, waveguide_type=s_right_type, transform=fp.translate(50.4, 0))
        # insts += s_mid_wg
        #
        # n+
        # elems += fp.el.Polygon([(50.4, 0), (50.4, 2.125), (71.4, 2.125), (71.4, 0), (70.4, 0), (68.4, 0.275), (53.4, 0.275), (51.4, 0)], layer=TECH.LAYER.)
#
