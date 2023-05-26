from dataclasses import dataclass
from fnpcell.pdk.technology import all as fpt
from IMECAS_pdk.technology.interfaces import CoreCladdingTrenchWaveguideType, Core2Cladding2WaveguideType
from IMECAS_pdk.technology.waveguide_factory import BendFactory, StraightFactory

Channel_C_COR_WIDTH = 0.45
Channel_C_CLD_WIDTH = 4.45
Channel_C_TCH_WIDTH = 2

Channel_O_COR_WIDTH = 0.38
Channel_O_CLD_WIDTH = 4.38
Channel_O_TCH_WIDTH = 2

RIB_C_COR_WIDTH = 0.65
RIB_C_CLD_WIDTH = 8.65
RIB_C_TCH_WIDTH = 4

RIB_O_COR_WIDTH = 0.58
RIB_O_CLD_WIDTH = 8.58
RIB_O_TCH_WIDTH = 4

RIB_C_SEFE_COR1_WIDTH = 1
RIB_C_SEFE_CLD1_WIDTH = 5
RIB_C_SEFE_COR2_WIDTH = 0.45
RIB_C_SEFE_CLD2_WIDTH = 4.45


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
        from IMECAS_pdk.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def core_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.FECOR

    @fpt.const_property
    def cladding_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.FECLD

    @fpt.const_property
    def trench_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.FETCH

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
        from IMECAS_pdk.technology import get_technology

        return get_technology().BAND.O

    @fpt.const_property
    def core_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.FECOR

    @fpt.const_property
    def cladding_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.FECLD

    @fpt.const_property
    def trench_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.FETCH

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class Rib_C(CoreCladdingTrenchWaveguideType):
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
        from IMECAS_pdk.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def core_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.SECOR

    @fpt.const_property
    def cladding_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.SECLD

    @fpt.const_property
    def trench_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.SETCH

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class Rib_O(CoreCladdingTrenchWaveguideType):
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
        from IMECAS_pdk.technology import get_technology

        return get_technology().BAND.O

    @fpt.const_property
    def core_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.SECOR

    @fpt.const_property
    def cladding_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.SECLD

    @fpt.const_property
    def trench_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.SETCH

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class Rib_C_SEFE(Core2Cladding2WaveguideType):
    @fpt.const_property
    def core1_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def cladding1_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def core2_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def cladding2_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def core1_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.FECOR

    @fpt.const_property
    def cladding1_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.FECLD

    @fpt.const_property
    def core_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.SECOR

    @fpt.const_property
    def cladding_layer(self):
        from IMECAS_pdk.technology import get_technology

        return get_technology().LAYER.SECLD

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
                        return BendFactory(radius_eff=10, waveguide_type=self)

                return WIRE()

            @fpt.staticconst
            def WIRE_TETM():
                @dataclass(frozen=True)
                class WIRE_TETM(__class__):
                    core_design_width: float = Channel_C_COR_WIDTH
                    cladding_design_width: float = Channel_C_CLD_WIDTH
                    trench_design_width: float = Channel_C_TCH_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND

                    @fpt.const_property
                    def BEND(self):
                        return BendFactory(radius_eff=10, waveguide_type=self)

                return WIRE_TETM()

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
                        return BendFactory(radius_eff=10, waveguide_type=self)

                return WIRE()

            @fpt.staticconst
            def WIRE_TETM():
                @dataclass(frozen=True)
                class WIRE_TETM(__class__):
                    core_design_width: float = Channel_O_COR_WIDTH
                    cladding_design_width: float = Channel_O_CLD_WIDTH
                    trench_design_width: float = Channel_O_TCH_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND

                    @fpt.const_property
                    def BEND(self):
                        return BendFactory(radius_eff=10, waveguide_type=self)


                return WIRE_TETM()

    class Rib:
        class C(Rib_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    core_design_width: float = RIB_C_COR_WIDTH
                    cladding_design_width: float = RIB_C_CLD_WIDTH
                    trench_design_width: float = RIB_C_TCH_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND

                    @fpt.const_property
                    def BEND(self):
                        return BendFactory(radius_eff=10, waveguide_type=self)


                return WIRE()

            @fpt.staticconst
            def WIRE_TETM():
                @dataclass(frozen=True)
                class WIRE_TETM(__class__):
                    core_design_width: float = RIB_C_COR_WIDTH
                    cladding_design_width: float = RIB_C_CLD_WIDTH
                    trench_design_width: float = RIB_C_TCH_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND

                    @fpt.const_property
                    def BEND(self):
                        return BendFactory(radius_eff=10, waveguide_type=self)

                return WIRE_TETM()

        class C_SEFE(Rib_C_SEFE):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    core1_design_width: float = RIB_C_SEFE_COR1_WIDTH
                    cladding1_design_width: float = RIB_C_SEFE_CLD1_WIDTH
                    core2_design_width: float = RIB_C_SEFE_COR2_WIDTH
                    cladding2_design_width: float = RIB_C_SEFE_CLD2_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND

                    @fpt.const_property
                    def BEND(self):
                        return BendFactory(radius_eff=10, waveguide_type=self)


                return WIRE()

            @fpt.staticconst
            def WIRE_TETM():
                @dataclass(frozen=True)
                class WIRE_TETM(__class__):
                    core1_design_width: float = RIB_C_SEFE_COR1_WIDTH
                    cladding1_design_width: float = RIB_C_SEFE_CLD1_WIDTH
                    core2_design_width: float = RIB_C_SEFE_COR2_WIDTH
                    cladding2_design_width: float = RIB_C_SEFE_CLD2_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND

                    @fpt.const_property
                    def BEND(self):
                        return BendFactory(radius_eff=10, waveguide_type=self)

                return WIRE_TETM()

        class O(Rib_O):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    core_design_width: float = RIB_O_COR_WIDTH
                    cladding_design_width: float = RIB_O_CLD_WIDTH
                    trench_design_width: float = RIB_O_TCH_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND

                    @fpt.const_property
                    def BEND(self):
                        return BendFactory(radius_eff=10, waveguide_type=self)

                return WIRE()

            @fpt.staticconst
            def WIRE_TETM():
                @dataclass(frozen=True)
                class WIRE_TETM(__class__):
                    core_design_width: float = RIB_O_COR_WIDTH
                    cladding_design_width: float = RIB_O_CLD_WIDTH
                    trench_design_width: float = RIB_O_TCH_WIDTH

                return WIRE_TETM()


if __name__ == "__main__":
    from pathlib import Path
    from fnpcell import all as fp
    from IMECAS_pdk.technology import get_technology

    TECH = get_technology()
    folder = Path(__file__).parent
    generated_folder = folder / "generated"
    csv_file = generated_folder / "wg.csv"
    # ================================

    fp.util.generate_csv_from_waveguides(csv_file=csv_file, waveguides=TECH.WG, overwrite=True)
