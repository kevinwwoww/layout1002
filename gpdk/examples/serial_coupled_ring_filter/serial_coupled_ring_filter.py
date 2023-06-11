import math
from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType

DEG2RAD = math.pi/180

@dataclass(eq=False)
class SerialCoupledRingFilter(fp.PCell):

    R1: float = fp.PositiveFloatParam(default=5, doc="radius of the long-axis of the ring")
    R2: float = fp.PositiveFloatParam(default=5.6, doc="radius of the bend coupler")
    R3: float = fp.PositiveFloatParam(default=3, doc="radius of the short-axis of the ring")
    w1: float = fp.PositiveFloatParam(default=0.45, doc="width of the ring waveguide")
    w2: float = fp.PositiveFloatParam(default=0.362, doc="width of the bus waveguide")
    # wh: float = fp.PositiveFloatParam(default=2, doc="width of the heater")
    # wm: float = fp.PositiveFloatParam(default=5, doc="width of the mental1")
    wgap: float = fp.PositiveFloatParam(default=0.15, doc="width of the inter-ring gap")
    theta: float = fp.PositiveFloatParam(default=56, doc="full angle of the long-axis segment")
    theta_coupled: float = fp.PositiveFloatParam(default=56, doc="full angle of the bend coupler")
    # theta_heater: float = fp.PositiveFloatParam(default=56, doc="full angle of the heater")
    xup: float = fp.NonNegFloatParam(default=0, doc="x coordinate of the input port")
    yup: float = fp.NonNegFloatParam(default=0, doc="y coordinate of the input port")
    ring_num: int = fp.PositiveIntParam(default=3, doc="number of the rings")
    straight_length: float = fp.PositiveFloatParam(default=5, doc="length of the fan-out waveguide")
    transition_length: float = fp.PositiveFloatParam(default=5, doc="length of the transition taper waveguide")

    waveguide_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    # port_names: fp.IPortOptions = fp.PortOptionsParam(count=6, default=["op_0", "op_1", "op_2", "op_3", "ep_0", "ep_1"])
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4, default=["top_left", "top_right", "bottom_left", "bottom_right"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        LAYER = TECH.LAYER
        R1 = self.R1
        R2 = self.R2
        R3 = self.R3
        w1 = self.w1
        w2 = self.w2
        # wh = self.wh
        wgap = self.wgap
        theta = self.theta
        xup = self.xup - (self.xup - 2 * self.R2 * math.sin(self.theta * DEG2RAD / 2) - self.straight_length)
        yup = self.yup - (self.yup + 2 * self.R2 * math.cos(self.theta * DEG2RAD / 2) - R2)
        ring_num = self.ring_num
        straight_length = self.straight_length

        xleft = xup - (R1 - R3) * math.sin(theta * DEG2RAD / 2)
        yleft = yup + (R1 - R3) * math.cos(theta * DEG2RAD / 2)
        xbottom = xup
        ybottom = 2 * yleft - yup
        xright = 2 * xup - xleft
        yright = yleft
        xoffset = 0
        yoffset = -(wgap + w1 + 2 * R1 - (ybottom - yup))
        
        waveguide_type = self.waveguide_type
        port_names = self.port_names

        core_layer = LAYER.FWG_COR
        cladding_layer = LAYER.FWG_CLD

        # si_etch2_layer = LAYER.SWG_COR
        # vl_layer = LAYER.VIA1_DRW
        # mh_layer = LAYER.TIN_DRW
        # m1_width = 6.0
        # m1_enc = 4.25
        # via_width = 5.0
        # via_height = 5.0
        # taper_big_end = 2.0
        # taper_small_end = 0.3
        # taper_length = 5.0  # FWG
        # w_mh = 2.0
        # min_mh_degrees = -75.0
        # max_mh_degrees = 255.0
        #
        # w_m1_out = m1_width
        # r_m1_out = ring_radius + m1_enc
        # r_mh = ring_radius
        # r_mh_in = r_mh - w_mh / 2
        #
        # w_si_3 = w_m1_out + r_m1_out * 2
        # h_si_3 = w_si_3
        #
        # core_width = waveguide_type.core_width
        #
        # x0 = 0
        # y0 = ring_radius + gap + core_width

        # add rings
        ###########
        # add rings
        ###########
        for i in range(ring_num):
            elems += fp.el.Arc(
                layer=core_layer,
                origin=(xup + i * xoffset, yup + i * yoffset),
                initial_degrees=90 - theta / 2,
                final_degrees=90 + theta / 2,
                radius=R1,
                stroke_width=w1,
            )
            elems += fp.el.Arc(
                layer=core_layer,
                origin=(xbottom + i * xoffset, ybottom + i * yoffset),
                initial_degrees=270 - theta / 2,
                final_degrees=270 + theta / 2,
                radius=R1,
                stroke_width=w1,
            )
            elems += fp.el.Arc(
                layer=core_layer,
                origin=(xleft + i * xoffset, yleft + i * yoffset),
                initial_degrees=180 - (180 - theta) / 2,
                final_degrees=180 + (180 - theta) / 2,
                radius=R3,
                stroke_width=w1,
            )
            elems += fp.el.Arc(
                layer=core_layer,
                origin=(xright + i * xoffset, yright + i * yoffset),
                initial_degrees=-(180 - theta) / 2,
                final_degrees=(180 - theta) / 2,
                radius=R3,
                stroke_width=w1,
            )

        ###################
        # add bend couplers
        ###################
        if self.theta_coupled != 180:
            theta = self.theta_coupled
            elems += fp.el.Arc(
                layer=core_layer,
                origin=(xup, yup),
                initial_degrees=90 - theta / 2,
                final_degrees=90 + theta / 2,
                radius=R2,
                stroke_width=w2,
            )
            elems += fp.el.Arc(
                layer=core_layer,
                origin=(xup, ybottom + (ring_num - 1) * yoffset),
                initial_degrees=270 - theta / 2,
                final_degrees=270 + theta / 2,
                radius=R2,
                stroke_width=w2,
            )

            ############################
            # add bend access waveguides
            ############################
            elems += fp.el.Arc(
                layer=core_layer,
                origin=(
                xup - 2 * R2 * math.sin(theta * DEG2RAD / 2), yup + 2 * R2 * math.cos(theta * DEG2RAD / 2)),
                initial_degrees=270,
                final_degrees=270 + theta / 2,
                radius=R2,
                stroke_width=w2,
            )
            elems += fp.el.Arc(
                layer=core_layer,
                origin=(
                    xup + 2 * R2 * math.sin(theta * DEG2RAD / 2),
                    yup + 2 * R2 * math.cos(theta * DEG2RAD / 2)),
                initial_degrees=270 - theta / 2,
                final_degrees=270,
                radius=R2,
                stroke_width=w2,
            )
            elems += fp.el.Arc(
                layer=core_layer,
                origin=(
                    xbottom - 2 * R2 * math.sin(theta * DEG2RAD / 2),
                    ybottom + (ring_num - 1) * yoffset - 2 * R2 * math.cos(theta * DEG2RAD / 2)),
                initial_degrees=90 - theta / 2,
                final_degrees=90,
                radius=R2,
                stroke_width=w2,
            )
            elems += fp.el.Arc(
                layer=core_layer,
                origin=(
                    xbottom + 2 * R2 * math.sin(theta * DEG2RAD / 2),
                    ybottom + (ring_num - 1) * yoffset - 2 * R2 * math.cos(theta * DEG2RAD / 2)),
                initial_degrees=90,
                final_degrees=90 + theta / 2,
                radius=R2,
                stroke_width=w2,
            )
        else:
            theta = 0

        #################################
        # add straight fan-out waveguides
        #################################
        # in
        xmax = xup - 2 * R2 * math.sin(theta * DEG2RAD / 2)
        xmin = xup - 2 * R2 * math.sin(theta * DEG2RAD / 2) - straight_length
        elems += fp.el.Rect(
            layer=core_layer,
            center=((xmax + xmin) / 2, yup + 2 * R2 * math.cos(theta * DEG2RAD / 2) - R2),
            width=xmax-xmin,
            height=w2,
        )
        begin_x_coord = xmin
        begin_y_coord = yup + 2 * R2 * math.cos(theta * DEG2RAD / 2) - R2
        end_x_coord = xmin - self.transition_length
        end_y_coord = yup + 2 * R2 * math.cos(theta * DEG2RAD / 2) - R2
        elems += fp.el.Line(
            # default direction: from left to right
            length=abs(begin_x_coord-end_x_coord),
            stroke_width=0.5,
            final_stroke_width=w2,
            layer=core_layer,
            anchor=fp.Anchor.CENTER,
            origin=((begin_x_coord+end_x_coord)/2, (begin_y_coord+end_y_coord)/2),
            # "origin" defines the cooridnate of the "anchor"
        )

        # through
        xmin = xup + 2 * R2 * math.sin(theta * DEG2RAD / 2)
        xmax = xup + 2 * R2 * math.sin(theta * DEG2RAD / 2) + straight_length
        elems += fp.el.Rect(
            layer=core_layer,
            center=((xmax + xmin) / 2, yup + 2 * R2 * math.cos(theta * DEG2RAD / 2) - R2),
            width=xmax - xmin,
            height=w2,
        )

        begin_x_coord = xmax
        begin_y_coord = yup + 2 * R2 * math.cos(theta * DEG2RAD / 2) - R2
        end_x_coord = xmax + self.transition_length
        end_y_coord = yup + 2 * R2 * math.cos(theta * DEG2RAD / 2) - R2
        elems += fp.el.Line(
            length=abs(begin_x_coord - end_x_coord),
            stroke_width=w2,
            final_stroke_width=0.5,
            layer=core_layer,
            anchor=fp.Anchor.CENTER,
            origin=((begin_x_coord + end_x_coord) / 2, (begin_y_coord + end_y_coord) / 2),
        )

        # drop
        xmax = xbottom - 2 * R2 * math.sin(theta * DEG2RAD / 2)
        xmin = xbottom - 2 * R2 * math.sin(theta * DEG2RAD / 2) - straight_length
        elems += fp.el.Rect(
            layer=core_layer,
            center=(
                (xmax + xmin) / 2,
                ybottom + (ring_num - 1) * yoffset - 2 * R2 * math.cos(theta * DEG2RAD / 2) + R2),
            width=xmax - xmin,
            height=w2,
        )

        begin_x_coord = xmin
        begin_y_coord = ybottom + (ring_num - 1) * yoffset - 2 * R2 * math.cos(theta * DEG2RAD / 2) + R2
        end_x_coord = xmin - self.transition_length
        end_y_coord = ybottom + (ring_num - 1) * yoffset - 2 * R2 * math.cos(theta * DEG2RAD / 2) + R2
        elems += fp.el.Line(
            length=abs(begin_x_coord - end_x_coord),
            stroke_width=0.5,
            final_stroke_width=w2,
            layer=core_layer,
            anchor=fp.Anchor.CENTER,
            origin=((begin_x_coord + end_x_coord) / 2, (begin_y_coord + end_y_coord) / 2),
        )

        # add
        xmin = xbottom + 2 * R2 * math.sin(theta * DEG2RAD / 2)
        xmax = xbottom + 2 * R2 * math.sin(theta * DEG2RAD / 2) + straight_length
        elems += fp.el.Rect(
            layer=core_layer,
            center=(
                (xmax + xmin) / 2,
                ybottom + (ring_num - 1) * yoffset - 2 * R2 * math.cos(theta * DEG2RAD / 2) + R2),
            width=xmax - xmin,
            height=w2,
        )
        begin_x_coord = xmax
        begin_y_coord = ybottom + (ring_num - 1) * yoffset - 2 * R2 * math.cos(theta * DEG2RAD / 2) + R2
        end_x_coord = xmax + self.transition_length
        end_y_coord = ybottom + (ring_num - 1) * yoffset - 2 * R2 * math.cos(theta * DEG2RAD / 2) + R2
        elems += fp.el.Line(
            length=abs(begin_x_coord - end_x_coord),
            stroke_width=w2,
            final_stroke_width=0.5,
            layer=core_layer,
            anchor=fp.Anchor.CENTER,
            origin=((begin_x_coord + end_x_coord) / 2, (begin_y_coord + end_y_coord) / 2),
        )

        # add cladding
        xmin = xup - 2 * R2 * math.sin(theta * DEG2RAD / 2) - straight_length - self.transition_length
        xmax = xbottom + 2 * R2 * math.sin(theta * DEG2RAD / 2) + straight_length + self.transition_length
        ymax = yup + R2 + 2.5 + 0.5
        ymin = ybottom + (ring_num - 1) * yoffset - R2 - 2.5 - 0.5
        elems += fp.el.Rect(
            layer=cladding_layer,
            center=((xmax + xmin) / 2, (ymax + ymin) / 2),
            width=xmax-xmin,
            height=ymax-ymin,
        )


        # ring = waveguide_type(curve=fp.g.EllipticalArc(radius=ring_radius, origin=(x0, y0))).with_ports((None, None)).with_name("ring")
        # insts += ring
        #
        # bus_length = w_si_3 + taper_length * 2
        # bus = waveguide_type(curve=fp.g.Line(length=bus_length, anchor=fp.Anchor.CENTER, origin=(0, 0))).with_name("bus")
        # insts += bus
        # y_offset = ring_radius * 2 + gap + gap_monitor + core_width * 2
        # monitor = waveguide_type(curve=fp.g.Line(length=bus_length, anchor=fp.Anchor.CENTER, origin=(0, y_offset))).with_name("monitor")
        # insts += monitor
        # rect = fp.el.Rect(width=w_si_3, height=h_si_3, layer=si_etch2_layer, center=(x0, y0))
        # elems += rect
        #
        # taper2 = fp.el.Line(
        #     length=taper_length, stroke_width=taper_big_end, final_stroke_width=taper_small_end, layer=si_etch2_layer, origin=(x0 + w_si_3 / 2, 0)
        # )
        # elems += taper2
        # taper3 = fp.el.Line(
        #     length=taper_length, stroke_width=taper_big_end, final_stroke_width=taper_small_end, layer=si_etch2_layer, origin=(x0 + w_si_3 / 2, y_offset)
        # )
        # elems += taper3
        # taper0 = fp.el.Line(
        #     length=taper_length,
        #     stroke_width=taper_small_end,
        #     final_stroke_width=taper_big_end,
        #     layer=si_etch2_layer,
        #     anchor=fp.Anchor.END,
        #     origin=(x0 - w_si_3 / 2, y_offset),
        # )
        # elems += taper0
        # taper1 = fp.el.Line(
        #     length=taper_length,
        #     stroke_width=taper_small_end,
        #     final_stroke_width=taper_big_end,
        #     layer=si_etch2_layer,
        #     anchor=fp.Anchor.END,
        #     origin=(x0 - w_si_3 / 2, 0),
        # )
        # elems += taper1
        # ring_mh = fp.el.EllipticalArc(
        #     radius=r_mh,
        #     stroke_width=w_mh,
        #     layer=mh_layer,
        #     final_degrees=max_mh_degrees - min_mh_degrees,
        #     transform=fp.rotate(degrees=min_mh_degrees).translate(x0, y0),
        # )
        # elems += ring_mh
        #
        # min_mh_radians = math.radians(min_mh_degrees)
        # dx = r_mh_in * math.cos(min_mh_radians)
        # dy = r_mh_in * math.sin(min_mh_radians)
        #
        # # TODO magic number 10
        # # VIA1 Layer
        # v1 = fp.el.Rect(width=via_width, height=via_height, layer=vl_layer, center=(dx + via_width, -10 + via_height / 2 - core_width / 2))
        # elems += v1
        # v2 = fp.el.Rect(width=via_width, height=via_height, layer=vl_layer, center=(-dx - via_width, -10 + via_height / 2 - core_width / 2))
        # elems += v2
        # # M2 Layer
        # m2 = fp.el.Rect(width=10, height=10, layer=LAYER.M2_DRW, center=(dx + via_width, -10 + via_height / 2 - core_width / 2))
        # elems += m2
        # m2 = fp.el.Rect(width=10, height=10, layer=LAYER.M2_DRW, center=(-dx - via_width, -10 + via_height / 2 - core_width / 2))
        # elems += m2
        # # VIA2 Layer
        # v1 = fp.el.Rect(width=via_width, height=via_height, layer=LAYER.VIA2_DRW, center=(dx + via_width, -10 + via_height / 2 - core_width / 2))
        # elems += v1
        # v2 = fp.el.Rect(width=via_width, height=via_height, layer=LAYER.VIA2_DRW, center=(-dx - via_width, -10 + via_height / 2 - core_width / 2))
        # elems += v2
        # # MT Layer
        # mt = fp.el.Rect(width=10, height=10, layer=LAYER.MT_DRW, center=(dx + via_width, -10 + via_height / 2 - core_width / 2))
        # elems += mt
        # mt = fp.el.Rect(width=10, height=10, layer=LAYER.MT_DRW, center=(-dx - via_width, -10 + via_height / 2 - core_width / 2))
        # elems += mt
        #
        # h_mh = y0 + dy + core_width / 2 + via_height / 2
        # mh1 = fp.el.Rect(width=w_mh, height=h_mh, layer=mh_layer, center=(dx + w_mh / 2, -core_width / 2 - 2.5 + h_mh / 2))
        # elems += mh1
        # mh2 = fp.el.Rect(width=w_mh, height=h_mh, layer=mh_layer, center=(-dx - w_mh / 2, -core_width / 2 - 2.5 + h_mh / 2))
        # elems += mh2
        # # magic number 10
        # mh1b = fp.el.Rect(width=10, height=10, layer=mh_layer, center=(-dx - 5, -core_width / 2 - via_height / 2 - 10 / 2))
        # elems += mh1b
        # mh2b = fp.el.Rect(width=10, height=10, layer=mh_layer, center=(dx + 5, -core_width / 2 - via_height / 2 - 10 / 2))
        # elems += mh2b
        #
        # top_start_ray, top_end_ray = monitor.curve.end_rays
        # bottom_start_ray, bottom_end_ray = bus.curve.end_rays
        #
        # pin1_x, pin1_y = (-dx - via_width, -10 + via_height / 2 - core_width / 2)
        # pin2_x, pin2_y = (dx + via_width, -10 + via_height / 2 - core_width / 2)

        ports += fp.Port(
            name=port_names[2],
            position=(xbottom - 2 * R2 * math.sin(theta * DEG2RAD / 2) - straight_length - self.transition_length,
                      ybottom + (ring_num - 1) * yoffset - 2 * R2 * math.cos(theta * DEG2RAD / 2) + R2),
            orientation=math.pi,
            waveguide_type=waveguide_type)
        ports += fp.Port(
            name=port_names[0],
            position=(xup - 2 * R2 * math.sin(theta * DEG2RAD / 2) - straight_length - self.transition_length,
                      yup + 2 * R2 * math.cos(theta * DEG2RAD / 2) - R2),
            orientation=math.pi,
            waveguide_type=waveguide_type)
        ports += fp.Port(
            name=port_names[3],
            position=(xbottom + 2 * R2 * math.sin(theta * DEG2RAD / 2) + straight_length + self.transition_length,
                      ybottom + (ring_num - 1) * yoffset - 2 * R2 * math.cos(theta * DEG2RAD / 2) + R2),
            orientation=0.0,
            waveguide_type=waveguide_type)
        ports += fp.Port(
            name=port_names[1],
            position=(xup + 2 * R2 * math.sin(theta * DEG2RAD / 2) + straight_length + self.transition_length,
                      yup + 2 * R2 * math.cos(theta * DEG2RAD / 2) - R2),
            orientation=0.0,
            waveguide_type=waveguide_type)

        return  insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += SerialCoupledRingFilter(ring_num=4, theta_coupled=180)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
