import math
from dataclasses import dataclass
from functools import cached_property

from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class AbstractSpiral(fp.IWaveguideLike, fp.PCell):
    total_length: float = fp.FloatParam()
    core_width: float = fp.FloatParam()
    spacing: float = fp.FloatParam()
    min_radius: float = fp.FloatParam()

    @cached_property
    def raw_curve(self):
        total_length = self.total_length
        inner_radius = self.min_radius
        stroke_width = self.core_width
        spacing = self.spacing
        #
        step = (spacing + stroke_width) / 2
        n = int((-(inner_radius - step / 2) + math.sqrt((inner_radius - step / 2) ** 2 - 2 * step * (-total_length / math.pi))) / step)
        #
        outer_radius = inner_radius + step * (n - 1)
        radius = outer_radius
        curve = fp.g.Path.move(to=(-radius, 0))
        for i in range(n):
            if i % 2 == 0:
                arc = fp.g.Arc(radius=radius, initial_degrees=180, final_degrees=360, origin=(0, 0))
            else:
                arc = fp.g.Arc(radius=radius, initial_degrees=0, final_degrees=180, origin=(step, 0))
            curve = curve.appended(arc)
            radius -= step
        #
        arc_length = total_length - curve.curve_length
        central_angle = arc_length / radius
        if fp.is_nonzero(central_angle):
            if n % 2 == 0:
                arc = fp.g.Arc(radius=radius, initial_degrees=180, final_radians=math.pi + central_angle, origin=(0, 0))
            else:
                arc = fp.g.Arc(radius=radius, initial_degrees=0, final_radians=0 + central_angle, origin=(step, 0))
            curve = curve.appended(arc)
        return curve


@dataclass(eq=False)
class Spiral(AbstractSpiral):
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()

    def _default_waveguide_type(self):
        TECH = get_technology()
        waveguide_type = TECH.WG.FWG.C.WIRE.updated(core_layout_width=self.core_width)
        return waveguide_type

    def build(self):
        insts, elems, ports = super().build()
        waveguide_type = self.waveguide_type
        curve = self.raw_curve
        #
        wg = waveguide_type(curve)
        insts += wg
        #
        ports += wg["op_0"]
        ports += wg["op_1"]

        return insts, elems, ports


@dataclass(eq=False)
class Terminator(AbstractSpiral):
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()

    def _default_waveguide_type(self):
        TECH = get_technology()
        waveguide_type = TECH.WG.FWG.C.WIRE.updated(core_layout_width=self.core_width).tapered(core_layout_width=0.2)  # end core width of this terminator
        return waveguide_type

    def build(self):
        insts, elems, ports = super().build()
        waveguide_type = self.waveguide_type
        curve = self.raw_curve
        #
        wg = waveguide_type(curve)
        insts += wg
        #
        ports += wg["op_0"]

        return insts, elems, ports


@dataclass(eq=False)
class ReverseSpiralChirpedBraggGrating(fp.PCell):
    total_length: float = fp.FloatParam(default=120000, locked=True)  # 12cm
    core_width: float = fp.FloatParam(default=2.8, locked=True)
    spacing: float = fp.FloatParam(default=30, locked=True)
    min_radius: float = fp.FloatParam(default=800, locked=True)

    start_period: float = fp.FloatParam(default=0.4046, locked=True)
    end_period: float = fp.FloatParam(default=0.3806, locked=True)

    def sampler(self, curve: fp.ICurve):
        SiN_length = curve.curve_length
        core_width = self.core_width
        start_period = self.start_period
        end_period = self.end_period
        number_of_rec = round(2 * SiN_length / (start_period + end_period)) - 1

        center_rec = (1 + number_of_rec) / 2  # where the center of the rectangle is

        for i in range(int(number_of_rec)):
            # x position of each rectangle
            rec_x_position = start_period * (i) - ((start_period - end_period) / number_of_rec) * ((1 + (i - 1)) * (i - 1) / 2)  # um
            # the x position of the center rectangle
            center_rec_x_position = start_period * center_rec - ((start_period - end_period) / number_of_rec) * ((1 + center_rec) * center_rec / 2)  # um
            # x position difference compare to the center rectangle, the modulated width from the Gaussian equation will be 0.015um at the center rectangle
            x_position_diff = center_rec_x_position - rec_x_position  # um
            # calculate the modulated width base on the equation, here the unit was changed to nm instead of um (need to be confirmed)
            height = 0.3 * math.e ** (-64 * ((x_position_diff / SiN_length) ** 4))
            pos = start_period * (i) - ((start_period - end_period) / number_of_rec) * ((1 + (i - 1)) * (i - 1) / 2) + 0.1
            rec = fp.el.Rect(
                width=0.2,
                height=core_width + height,
                center=(0, 0),
                layer=TECH.LAYER.FWG_COR,
            )
            yield pos, rec

    def build(self):
        insts, elems, ports = super().build()
        #
        spiral = Spiral(total_length=self.total_length, core_width=self.core_width, spacing=self.spacing, min_radius=self.min_radius)
        insts += spiral
        #
        terminator = Terminator(total_length=700, core_width=self.core_width, spacing=10, min_radius=20)  # arbitary parameters, just for demo
        insts += fp.place(terminator, "op_0", at=spiral["op_1"])
        #
        paint = fp.el.CurvePaint.Sampling(sampler=self.sampler)
        elems += paint(spiral.curve)
        #
        ports += spiral["op_0"]
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    device = ReverseSpiralChirpedBraggGrating()
    library += device

    # fmt: on
    # ==============================================================

    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
