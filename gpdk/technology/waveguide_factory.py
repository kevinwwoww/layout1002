import math
from dataclasses import dataclass, field

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt


@dataclass(frozen=True)
class StraightFactory(fpt.IStraightWaveguideFactory):
    def __call__(self, type: fpt.IWaveguideType, length: float):
        from gpdk.components.straight.straight import Straight

        straight = Straight(length=length, waveguide_type=type)
        return straight, ("op_0", "op_1")


@dataclass(frozen=True)
class CircularBendFactory(fpt.IBendWaveguideFactory):
    radius_eff: float
    waveguide_type: fpt.IWaveguideType = field(repr=False)

    def __call__(self, central_angle: float):
        from gpdk.components.bend.bend_circular import BendCircular, BendCircular90_FWG_C_WIRE, BendCircular90_FWG_C_EXPANDED
        from gpdk.technology import get_technology

        TECH = get_technology()

        radius_eff = self.radius_eff

        bend = None
        if fp.is_close(abs(central_angle), math.pi / 2):
            if self.waveguide_type == TECH.WG.FWG.C.WIRE:
                bend = BendCircular90_FWG_C_WIRE()
            elif self.waveguide_type == TECH.WG.FWG.C.EXPANDED:
                bend = BendCircular90_FWG_C_EXPANDED()

            if bend and central_angle < 0:
                bend = bend.v_mirrored()

        if bend is None:
            bend = BendCircular(degrees=math.degrees(central_angle), radius=radius_eff, waveguide_type=self.waveguide_type)

        return bend, radius_eff, ("op_0", "op_1")


@dataclass(frozen=True)
class EulerBendFactory(fpt.IBendWaveguideFactory):
    radius_min: float
    l_max: float
    waveguide_type: fpt.IWaveguideType = field(repr=False)

    def __call__(self, central_angle: float):
        from gpdk.components.bend.bend_euler import BendEuler, BendEuler90, BendEuler90_FWG_C_WIRE, BendEuler90_FWG_C_EXPANDED
        from gpdk.technology.interfaces import CoreCladdingWaveguideType
        from gpdk.technology import get_technology

        TECH = get_technology()

        bend = None
        if fp.is_close(abs(central_angle), math.pi / 2):
            if self.waveguide_type == TECH.WG.FWG.C.WIRE:
                bend = BendEuler90_FWG_C_WIRE()
            elif self.waveguide_type == TECH.WG.FWG.C.EXPANDED:
                bend = BendEuler90_FWG_C_EXPANDED()
            elif isinstance(self.waveguide_type, CoreCladdingWaveguideType):
                bend = BendEuler90(slab_square=True, radius_min=self.radius_min, l_max=self.l_max, waveguide_type=self.waveguide_type)

            if bend and central_angle < 0:
                bend = bend.v_mirrored()

        if bend is None:
            bend = BendEuler(degrees=math.degrees(central_angle), radius_min=self.radius_min, l_max=self.l_max, waveguide_type=self.waveguide_type)

        return bend, bend.raw_curve.radius_eff, ("op_0", "op_1")
