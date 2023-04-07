import math
from dataclasses import dataclass, field

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt


@dataclass(frozen=True)
class StraightFactory(fpt.IStraightWaveguideFactory):
    def __call__(self, type: fpt.IWaveguideType, length: float):
        from IMECAS_SiN_pdk_1_0_0.components.straight.straight import Straight

        straight = Straight(length=length, waveguide_type=type)
        return straight, ("op_0", "op_1")


@dataclass(frozen=True)
class BendFactory(fpt.IBendWaveguideFactory):
    radius_eff: float
    waveguide_type: fpt.IWaveguideType = field(repr=False, compare=False)

    def __call__(self, central_angle: float):
        from IMECAS_SiN_pdk_1_0_0.components.bend.bend_circular import Bend, Bend_O, Bend_C
        from IMECAS_SiN_pdk_1_0_0.technology import get_technology

        TECH = get_technology()

        radius_eff = self.radius_eff

        bend = None
        if fp.is_close(abs(central_angle), math.pi / 2):
            if self.waveguide_type == TECH.WG.Channel.C.WIRE:
                bend = Bend_C()
            elif self.waveguide_type == TECH.WG.Channel.O.WIRE:
                bend = Bend_O()

            if bend and central_angle < 0:
                bend = bend.v_mirrored()

        if bend is None:
            bend = Bend(degrees=math.degrees(central_angle), radius=radius_eff,
                        waveguide_type=self.waveguide_type)

        return bend, radius_eff, ("op_0", "op_1")


@dataclass(frozen=True)
class bb_C_BendFactory(fpt.IBendWaveguideFactory):
    waveguide_type: fpt.IWaveguideType = field(repr=False, compare=False)

    def __call__(self, central_angle: float):

        from IMECAS_SiN_pdk_1_0_0.technology import get_technology
        from IMECAS_SiN_pdk_1_0_0.components.bb_Bend.SIN_Bend_C import SIN_Bend_C_new

        TECH = get_technology()

        radius_eff = 100
        bend = SIN_Bend_C_new()

        print(central_angle)

        if central_angle < 0:
            bend = bend.v_mirrored()

        print(bend)
        return bend, radius_eff, ("in1", "out1")


@dataclass(frozen=True)
class bb_O_BendFactory(fpt.IBendWaveguideFactory):
    waveguide_type: fpt.IWaveguideType = field(repr=False, compare=False)

    def __call__(self, central_angle: float):

        from IMECAS_SiN_pdk_1_0_0.technology import get_technology
        from IMECAS_SiN_pdk_1_0_0.components.bb_Bend.SIN_Bend_O import SIN_Bend_O_new

        TECH = get_technology()

        radius_eff = 100
        bend = SIN_Bend_O_new()

        print(central_angle)

        if central_angle < 0:
            bend = bend.v_mirrored()

        print(bend)
        return bend, radius_eff, ("in1", "out1")