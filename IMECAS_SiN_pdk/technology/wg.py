from dataclasses import dataclass

from fnpcell.pdk.technology import all as fpt
from IMECAS_SiN_pdk.technology.interfaces import CoreCladdingTrenchWaveguideType
from IMECAS_SiN_pdk.technology.waveguide_factory import BendFactory, StraightFactory

# from IMECAS_SiN_pdk import all as pdk

Channel_C_COR_WIDTH = 1.5
Channel_C_CLD_WIDTH = 21.5
Channel_C_TCH_WIDTH = 10

Channel_O_COR_WIDTH = 1.1
Channel_O_CLD_WIDTH = 21.1
Channel_O_TCH_WIDTH = 10


@fpt.hash_code
@dataclass(frozen=True)
class Channel_C(CoreCladdingTrenchWaveguideType):
    @fpt.const_property
    def core_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def cladding_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def trench_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from IMECAS_SiN_pdk.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def core_layer(self):
        from IMECAS_SiN_pdk.technology import get_technology

        return get_technology().LAYER.SINCOR

    @fpt.const_property
    def cladding_layer(self):
        from IMECAS_SiN_pdk.technology import get_technology

        return get_technology().LAYER.SINCLD

    @fpt.const_property
    def trench_layer(self):
        from IMECAS_SiN_pdk.technology import get_technology

        return get_technology().LAYER.SINTCH

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class Channel_O(CoreCladdingTrenchWaveguideType):
    @fpt.const_property
    def core_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def cladding_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def trench_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from IMECAS_SiN_pdk.technology import get_technology

        return get_technology().BAND.O

    @fpt.const_property
    def core_layer(self):
        from IMECAS_SiN_pdk.technology import get_technology

        return get_technology().LAYER.SINCOR

    @fpt.const_property
    def cladding_layer(self):
        from IMECAS_SiN_pdk.technology import get_technology

        return get_technology().LAYER.SINCLD

    @fpt.const_property
    def trench_layer(self):
        from IMECAS_SiN_pdk.technology import get_technology

        return get_technology().LAYER.SINTCH

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


#######################################################################################################################
# WG                                                                                                                  #
#######################################################################################################################


class WG:
    class Channel:
        class C(Channel_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    core_design_width: float = Channel_C_COR_WIDTH
                    cladding_design_width: float = Channel_C_CLD_WIDTH
                    trench_design_width: float = Channel_C_TCH_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND

                    @fpt.const_property
                    def BEND(self):
                        return BendFactory(radius_eff=100, waveguide_type=self)



                return WIRE()

        class O(Channel_O):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    core_design_width: float = Channel_O_COR_WIDTH
                    cladding_design_width: float = Channel_O_CLD_WIDTH
                    trench_design_width: float = Channel_O_TCH_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND

                    @fpt.const_property
                    def BEND(self):
                        return BendFactory(radius_eff=100, waveguide_type=self)


                return WIRE()


if __name__ == "__main__":
    from pathlib import Path
    from fnpcell import all as fp
    from IMECAS_SiN_pdk.technology import get_technology

    TECH = get_technology()
    folder = Path(__file__).parent
    generated_folder = folder / "generated"
    csv_file = generated_folder / "wg.csv"
    # ================================

    fp.util.generate_csv_from_waveguides(csv_file=csv_file, waveguides=TECH.WG, overwrite=True)
