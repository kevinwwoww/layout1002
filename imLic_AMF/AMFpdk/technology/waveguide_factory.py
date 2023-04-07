import math
from dataclasses import dataclass, field

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt


@dataclass(frozen=True)
class StraightFactory(fpt.IStraightWaveguideFactory):
    def __call__(self, type: fpt.IWaveguideType, length: float):
        from AMFpdk.components.straight.straight import Straight

        straight = Straight(length=length, waveguide_type=type)
        return straight, ("op_0", "op_1")


@dataclass(frozen=True)
class CircularBendFactory(fpt.IBendWaveguideFactory):
    radius_eff: float
    waveguide_type: fpt.IWaveguideType = field(repr=False, compare=False)

    def __call__(self, central_angle: float):
        from AMFpdk.components.bend.bend_circular import BendCircular, BendCircular90
        from AMFpdk.technology import get_technology

        TECH = get_technology()

        radius_eff = self.radius_eff

        bend = None
        if fp.is_close(abs(central_angle), math.pi / 2):
            if self.waveguide_type == TECH.WG.SLAB.C.WIRE:
                bend = BendCircular90()



            if bend and central_angle < 0:
                bend = bend.v_mirrored()

        if bend is None:
            bend = BendCircular(degrees=math.degrees(central_angle), radius=radius_eff,
                                waveguide_type=self.waveguide_type)

        return bend, radius_eff, ("op_0", "op_1")


@dataclass(frozen=True)
class EulerBendFactory(fpt.IBendWaveguideFactory):
    radius_min: float
    l_max: float
    waveguide_type: fpt.IWaveguideType = field(repr=False, compare=False)

    def __call__(self, central_angle: float):
        from AMFpdk.components.bend.bend_euler import BendEuler, BendEuler90
        from AMFpdk.technology.interfaces import CoreWaveguideType
        from AMFpdk.technology import get_technology

        TECH = get_technology()

        bend = None

        if fp.is_close(abs(central_angle), math.pi / 2):
            if self.waveguide_type == TECH.WG.SLAB.C.WIRE:
                bend = BendEuler90()
            elif isinstance(self.waveguide_type, CoreWaveguideType):
                bend = BendEuler90(slab_square=True, radius_min=self.radius_min, l_max=self.l_max,
                                   waveguide_type=self.waveguide_type)

            if bend and central_angle < 0:
                bend = bend.v_mirrored()

        if bend is None:
            bend = BendEuler(degrees=math.degrees(central_angle),
                             radius_min=self.radius_min,
                             l_max=self.l_max,
                             waveguide_type=self.waveguide_type)

        return bend, bend.raw_curve.radius_eff, ("op_0", "op_1")
