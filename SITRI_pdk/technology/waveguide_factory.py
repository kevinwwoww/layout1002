import math
from dataclasses import dataclass, field

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt


@dataclass(frozen=True)
class StraightFactory(fpt.IStraightWaveguideFactory):
    def __call__(self, type: fpt.IWaveguideType, length: float):
        from SITRI_pdk.components.straight.straight import Straight

        straight = Straight(Length=length, waveguide_type=type)
        return straight, ("op_0", "op_1")


@dataclass(frozen=True)
class CircularBendFactory(fpt.IBendWaveguideFactory):
    radius_eff: float
    waveguide_type: fpt.IWaveguideType = field(repr=False, compare=False)

    def __call__(self, central_angle: float):
        from SITRI_pdk.components.bend.bend_circular import Bend, Bend90
        from SITRI_pdk.technology import get_technology

        TECH = get_technology()

        radius_eff = self.radius_eff

        bend = None
        if fp.is_close(abs(central_angle), math.pi / 2):
            if self.waveguide_type == TECH.WG.CHANNEL.C.WIRE:
                bend = Bend90()

            if bend and central_angle < 0:
                bend = bend.v_mirrored()

        if bend is None:
            bend = Bend(EndAngle=math.degrees(central_angle), Radius=self.radius_eff,
                        waveguide_type=self.waveguide_type)
        # if central_angle < 0:
        #     bend = bend.v_mirrored()

        print(central_angle)
        print(self.radius_eff)

        return bend, radius_eff, ("op_0", "op_1")
