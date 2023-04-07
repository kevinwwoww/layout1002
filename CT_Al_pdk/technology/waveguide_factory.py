import math
from dataclasses import dataclass, field

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt


@dataclass(frozen=True)
class StraightFactory(fpt.IStraightWaveguideFactory):
    def __call__(self, type: fpt.IWaveguideType, length: float):
        from CT_Al_pdk.components.straight.straight import Straight

        straight = Straight(length=length, waveguide_type=type)
        return straight, ("op_0", "op_1")


@dataclass(frozen=True)
class CircularBendFactory(fpt.IBendWaveguideFactory):
    radius_eff: float
    waveguide_type: fpt.IWaveguideType = field(repr=False, compare=False)

    def __call__(self, central_angle: float):
        from CT_Al_pdk.components.bend.bend_circular import BendCircular, BendCircular90_Rib_WG_C_WIRE, BendCircular90_Strip_WG_C_WIRE
        from CT_Al_pdk.technology import get_technology

        TECH = get_technology()

        radius_eff = self.radius_eff

        bend = None
        if fp.is_close(abs(central_angle), math.pi / 2):
            if self.waveguide_type == TECH.WG.Strip_WG.C.WIRE:
                bend = BendCircular90_Strip_WG_C_WIRE()
            elif self.waveguide_type == TECH.WG.Rib_WG.C.WIRE:
                bend = BendCircular90_Rib_WG_C_WIRE()

            if bend and central_angle < 0:
                bend = bend.v_mirrored()

        if bend is None:
            bend = BendCircular(degrees=math.degrees(central_angle), radius=radius_eff,
                                waveguide_type=self.waveguide_type)

        print(bend, radius_eff)
        return bend, radius_eff, ("op_0", "op_1")


@dataclass(frozen=True)
class EulerBendFactory(fpt.IBendWaveguideFactory):
    radius_min: float
    l_max: float
    waveguide_type: fpt.IWaveguideType = field(repr=False, compare=False)

    def __call__(self, central_angle: float):
        from CT_Al_pdk.components.bend.bend_euler import BendEuler, BendEuler90, BendEuler90_Rib_WG_C_WIRE, BendEuler90_Strip_WG_C_WIRE
        from CT_Al_pdk.technology.interfaces import CoreWaveguideType
        from CT_Al_pdk.technology import get_technology

        TECH = get_technology()

        bend = None
        if fp.is_close(abs(central_angle), math.pi / 2):
            if self.waveguide_type == TECH.WG.Strip_WG.C.WIRE:
                bend = BendEuler90_Strip_WG_C_WIRE()
            elif self.waveguide_type == TECH.WG.Rib_WG.C.WIRE:
                bend = BendEuler90_Rib_WG_C_WIRE()
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
