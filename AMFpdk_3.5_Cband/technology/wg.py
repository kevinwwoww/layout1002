from dataclasses import dataclass

from fnpcell.pdk.technology import all as fpt
from AMFpdk_3_5_Cband.technology.interfaces import CoreWaveguideType, SlabWaveguideType
from AMFpdk_3_5_Cband.technology.waveguide_factory import StraightFactory, CircularBendFactory, EulerBendFactory

# from  gpdk_AMF.technology.waveguide_factory import CircularBendFactory, EulerBendFactory, StraightFactory
"""channel WG only need to define RIB layer"""
"""rib WG need to define RIB layer + SLAB layer"""

RIB_WIDTH = 0.5
GRAT_WIDTH = 1.0
SLAB_WIDTH = 2.0

RIB_SIM_WL = [1.4, 1.5, 1.6]
RIB_SIM_NEFF = [2.5066666, 2.4, 2.2933333]
RIB_SIM_LOSS = [1, 1, 1]

GRAT_SIM_WL = [1.4, 1.5, 1.6]
GRAT_SIM_NEFF = [2.5066666, 2.4, 2.2933333]
GRAT_SIM_LOSS = [1, 1, 1]

SLAB_SIM_WL = [1.4, 1.5, 1.6]
SLAB_SIM_NEFF = [2.5066666, 2.4, 2.2933333]
SLAB_SIM_LOSS = [1, 1, 1]


@fpt.hash_code
@dataclass(frozen=True)
class CHANNEL_C(CoreWaveguideType):
    @fpt.const_property
    def wg_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from AMFpdk_3_5_Cband.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def wg_layer(self):
        from AMFpdk_3_5_Cband.technology import get_technology

        return get_technology().LAYER.RIB

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class RIB_C(SlabWaveguideType):
    @fpt.const_property
    def wg_slab_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def wg_rib_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from AMFpdk_3_5_Cband.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def wg_slab_layer(self):
        from AMFpdk_3_5_Cband.technology import get_technology
        return get_technology().LAYER.SLAB

    @fpt.const_property
    def wg_layer(self):
        from AMFpdk_3_5_Cband.technology import get_technology
        return get_technology().LAYER.RIB

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


class WG:
    class CHANNEL:
        class C(CHANNEL_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    wg_design_width: float = RIB_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_CIRCULAR

                    #
                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=5, waveguide_type=self)

                return WIRE()

    class RIB:
        class C(RIB_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    wg_rib_design_width: float = RIB_WIDTH
                    wg_slab_design_width: float = SLAB_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_CIRCULAR

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=20, waveguide_type=self)

                return WIRE()


if __name__ == "__main__":
    from pathlib import Path
    from fnpcell import all as fp
    from AMFpdk_3_5_Cband.technology import get_technology

    TECH = get_technology()
    folder = Path(__file__).parent
    generated_folder = folder / "generated_AMF"
    csv_file = generated_folder / "wg.csv"

    fp.util.generate_csv_from_waveguides(csv_file=csv_file, waveguides=TECH.WG, overwrite=True)
