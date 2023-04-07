from dataclasses import dataclass

from fnpcell.pdk.technology import all as fpt
from CT_pCu_pdk.technology.interfaces import CoreWaveguideType, SlabWaveguideType
from CT_pCu_pdk.technology.waveguide_factory import StraightFactory, CircularBendFactory, EulerBendFactory

# from  CT_Cu_pdk_AMF.technology.waveguide_factory import CircularBendFactory, EulerBendFactory, StraightFactory

Hard_Mask_WG_C_WIRE_WIDTH = 0.45
Hard_Mask_WG_O_WIRE_WIDTH = 0.41

Rib_WG_C_WIRE_WIDTH = 2
Rib_WG_O_WIRE_WIDTH = 2

Strip_WG_C_WIRE_WIDTH = 2.1
Strip_WG_O_WIRE_WIDTH = 2.1

Hard_Mask_PC_WIDTH = 0.5
Si_PC_grating_WIDTH = 0.5
SiN_WG_WIDTH = 1



@fpt.hash_code
@dataclass(frozen=True)
class Strip_WG_C(CoreWaveguideType):
    @fpt.const_property
    def wg_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from CT_pCu_pdk.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def wg_layer(self):
        from CT_pCu_pdk.technology import get_technology

        return get_technology().LAYER.Hard_Mask_WG

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class Strip_WG_O(CoreWaveguideType):
    @fpt.const_property
    def wg_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from CT_pCu_pdk.technology import get_technology

        return get_technology().BAND.O

    @fpt.const_property
    def wg_layer(self):
        from CT_pCu_pdk.technology import get_technology

        return get_technology().LAYER.Hard_Mask_WG

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class SiN_WG_C(CoreWaveguideType):
    @fpt.const_property
    def wg_bias(self):
        return fpt.CDBiasLinear(0.1)

    @fpt.const_property
    def band(self):
        from CT_pCu_pdk.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def wg_layer(self):
        from CT_pCu_pdk.technology import get_technology

        return get_technology().LAYER.SiN_WG

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class SiN_WG_O(CoreWaveguideType):
    @fpt.const_property
    def wg_bias(self):
        return fpt.CDBiasLinear(0.1)

    @fpt.const_property
    def band(self):
        from CT_pCu_pdk.technology import get_technology

        return get_technology().BAND.O

    @fpt.const_property
    def wg_layer(self):
        from CT_pCu_pdk.technology import get_technology

        return get_technology().LAYER.SiN_WG

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class Rib_WG_C(SlabWaveguideType):
    @fpt.const_property
    def hm_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def rib_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def strip_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from CT_pCu_pdk.technology import get_technology
        return get_technology().BAND.C

    @fpt.const_property
    def wg_layer(self):
        from CT_pCu_pdk.technology import get_technology
        return get_technology().LAYER.Hard_Mask_WG

    @fpt.const_property
    def rib_layer(self):
        from CT_pCu_pdk.technology import get_technology
        return get_technology().LAYER.Rib_WG

    @fpt.const_property
    def strip_layer(self):
        from CT_pCu_pdk.technology import get_technology
        return get_technology().LAYER.Strip_WG

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class Rib_WG_O(SlabWaveguideType):
    @fpt.const_property
    def hm_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def rib_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def strip_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from CT_pCu_pdk.technology import get_technology
        return get_technology().BAND.O

    @fpt.const_property
    def wg_layer(self):
        from CT_pCu_pdk.technology import get_technology
        return get_technology().LAYER.Hard_Mask_WG

    @fpt.const_property
    def rib_layer(self):
        from CT_pCu_pdk.technology import get_technology
        return get_technology().LAYER.Rib_WG

    @fpt.const_property
    def strip_layer(self):
        from CT_pCu_pdk.technology import get_technology
        return get_technology().LAYER.Strip_WG

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


#######################################################################################################################
# WG                                                                                                                  #
#######################################################################################################################
radius = 5


class WG:
    class Strip_WG:
        class C(Strip_WG_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    wg_design_width: float = Hard_Mask_WG_C_WIRE_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_EULER

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=radius, waveguide_type=self)

                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=radius, l_max=5, waveguide_type=self)

                return WIRE()

        class O(Strip_WG_O):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    wg_design_width: float = Hard_Mask_WG_O_WIRE_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_EULER

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=radius, waveguide_type=self)

                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=radius, l_max=5, waveguide_type=self)

                return WIRE()

    class SiN_WG:
        class C(SiN_WG_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    wg_design_width: float = SiN_WG_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_EULER

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=radius, waveguide_type=self)

                    #
                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=radius, l_max=5, waveguide_type=self)

                return WIRE()

        class O(SiN_WG_O):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    wg_design_width: float = SiN_WG_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_EULER

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=radius, waveguide_type=self)

                    #
                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=radius, l_max=5, waveguide_type=self)

                return WIRE()

    class Rib_WG:
        class C(Rib_WG_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    hm_design_width: float = Hard_Mask_WG_C_WIRE_WIDTH
                    rib_design_width: float = Rib_WG_C_WIRE_WIDTH
                    strip_design_width: float = Strip_WG_C_WIRE_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_EULER

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=radius, waveguide_type=self)

                    #
                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=radius, l_max=5, waveguide_type=self)

                return WIRE()

        class O(Rib_WG_O):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    hm_design_width: float = Hard_Mask_WG_O_WIRE_WIDTH
                    rib_design_width: float = Rib_WG_O_WIRE_WIDTH
                    strip_design_width: float = Strip_WG_O_WIRE_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_EULER

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=radius, waveguide_type=self)

                    #
                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=radius, l_max=5, waveguide_type=self)

                return WIRE()


if __name__ == "__main__":
    from pathlib import Path
    from fnpcell import all as fp
    from CT_pCu_pdk.technology import get_technology

    TECH = get_technology()
    folder = Path(__file__).parent
    generated_folder = folder / "generated"
    csv_file = generated_folder / "wg.csv"
    # ================================

    fp.util.generate_csv_from_waveguides(csv_file=csv_file, waveguides=TECH.WG, overwrite=True)
    TECH.WG.Strip_WG.C.WIRE
