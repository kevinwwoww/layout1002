from dataclasses import dataclass

from fnpcell.pdk.technology import all as fpt
from fpdk.technology.interfaces import CoreCladdingWaveguideType, SlotWaveguideType, SwgWaveguideType
from fpdk.technology.waveguide_factory import CircularBendFactory, EulerBendFactory, StraightFactory

FWG_C_WIRE_WIDTH = 0.45
FWG_C_EXPANDED_WIDTH = 0.8
FWG_C_TRENCH_WIDTH = 2.0

FWG_C_WIRE_SIM_WL = [1.4, 1.5, 1.6]
FWG_C_WIRE_SIM_NEFF = [2.5066666, 2.4, 2.2933333]
FWG_C_WIRE_SIM_LOSS = [1, 1, 1]

FWG_C_EXPANDED_SIM_WL = [1.4, 1.5, 1.6]
FWG_C_EXPANDED_SIM_NEFF = [2.5066666, 2.4, 2.2933333]
FWG_C_EXPANDED_SIM_LOSS = [2, 2, 2]

MWG_C_WIRE_WIDTH = 1
MWG_C_EXPANDED_WIDTH = 1.5
MWG_C_TRENCH_WIDTH = 5.0

MWG_C_WIRE_SIM_WL = [1.4, 1.5, 1.6]
MWG_C_WIRE_SIM_NEFF = [2.5066666, 2.4, 2.2933333]
MWG_C_WIRE_SIM_LOSS = [1, 1, 1]

MWG_C_EXPANDED_SIM_WL = [1.4, 1.5, 1.6]
MWG_C_EXPANDED_SIM_NEFF = [2.5066666, 2.4, 2.2933333]
MWG_C_EXPANDED_SIM_LOSS = [1, 1, 1]

SWG_C_WIRE_WIDTH = 1.0
SWG_C_EXPANDED_WIDTH = 1.5
SWG_C_TRENCH_WIDTH = 5.0

SWG_C_WIRE_SIM_WL = [1.4, 1.5, 1.6]
SWG_C_WIRE_SIM_NEFF = [2.5066666, 2.4, 2.2933333]
SWG_C_WIRE_SIM_LOSS = [1, 1, 1]

SWG_C_EXPANDED_SIM_WL = [1.4, 1.5, 1.6]
SWG_C_EXPANDED_SIM_NEFF = [2.5066666, 2.4, 2.2933333]
SWG_C_EXPANDED_SIM_LOSS = [1, 1, 1]

WIRE_TETM_RATIO = 1.2
EXPANDED_TETM_RATIO = 2.0

O_BAND_RATIO = 0.8


@fpt.hash_code
@dataclass(frozen=True)
class FWG_C(CoreCladdingWaveguideType):
    @fpt.const_property
    def core_bias(self):
        return fpt.CDBiasLinear(0.1)

    @fpt.const_property
    def cladding_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from fpdk.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def core_layer(self):
        from fpdk.technology import get_technology

        return get_technology().LAYER.FWG_COR

    @fpt.const_property
    def cladding_layer(self):
        from fpdk.technology import get_technology

        return get_technology().LAYER.FWG_CLD

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()



@fpt.hash_code
@dataclass(frozen=True)
class SWG_C(CoreCladdingWaveguideType):
    @fpt.const_property
    def core_bias(self):
        return fpt.CDBiasLinear([(0.4, 0.1), (0.6, 0.15)])

    @fpt.const_property
    def cladding_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from fpdk.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def core_layer(self):
        from fpdk.technology import get_technology

        return get_technology().LAYER.SWG_COR

    @fpt.const_property
    def cladding_layer(self):
        from fpdk.technology import get_technology

        return get_technology().LAYER.SWG_CLD

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()



#



#######################################################################################################################
# WG                                                                                                                  #
#######################################################################################################################


class WG:
    class FWG:
        class C(FWG_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    core_design_width: float = FWG_C_WIRE_WIDTH
                    cladding_design_width: float = FWG_C_WIRE_WIDTH + FWG_C_TRENCH_WIDTH * 2

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_EULER

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=self.cladding_width / 2 + 1, waveguide_type=self)

                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=self.cladding_width / 2 + 1, l_max=5, waveguide_type=self)

                    @fpt.const_property
                    def theoretical_parameters(self):
                        if self == WG.FWG.C.WIRE:
                            return fpt.sim.TheoreticalParameters(wl=FWG_C_WIRE_SIM_WL, n_eff=FWG_C_WIRE_SIM_NEFF, loss=FWG_C_WIRE_SIM_LOSS)
                        raise NotImplementedError("No theoretical parameters for this updated waveguide-type")

                return WIRE()

            @fpt.staticconst
            def EXPANDED():
                @dataclass(frozen=True)
                class EXPANDED(__class__):
                    core_design_width: float = FWG_C_EXPANDED_WIDTH
                    cladding_design_width: float = FWG_C_EXPANDED_WIDTH + FWG_C_TRENCH_WIDTH * 2

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_EULER

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=self.cladding_width / 2 + 1, waveguide_type=self)

                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=self.cladding_width / 2 + 1, l_max=10, waveguide_type=self)

                    @fpt.const_property
                    def theoretical_parameters(self):
                        if self == WG.FWG.C.EXPANDED:
                            return fpt.sim.TheoreticalParameters(wl=FWG_C_EXPANDED_SIM_WL, n_eff=FWG_C_EXPANDED_SIM_NEFF, loss=FWG_C_EXPANDED_SIM_LOSS)
                        raise NotImplementedError("No theoretical parameters for this updated waveguide-type")

                return EXPANDED()


    class SWG:
        class C(SWG_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    core_design_width: float = SWG_C_WIRE_WIDTH
                    cladding_design_width: float = SWG_C_WIRE_WIDTH + SWG_C_TRENCH_WIDTH * 2

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_EULER

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=self.cladding_width / 2 + 1, waveguide_type=self)

                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=self.cladding_width / 2 + 1, l_max=15, waveguide_type=self)

                    @fpt.const_property
                    def theoretical_parameters(self):
                        return fpt.sim.TheoreticalParameters(wl=SWG_C_WIRE_SIM_WL, n_eff=SWG_C_WIRE_SIM_NEFF, loss=SWG_C_WIRE_SIM_LOSS)


                return WIRE()


            @fpt.staticconst
            def EXPANDED():
                @dataclass(frozen=True)
                class EXPANDED(__class__):
                    core_design_width: float = SWG_C_EXPANDED_WIDTH * EXPANDED_TETM_RATIO
                    cladding_design_width: float = SWG_C_EXPANDED_WIDTH * EXPANDED_TETM_RATIO + SWG_C_TRENCH_WIDTH * 2

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_EULER

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=self.cladding_width / 2 + 1, waveguide_type=self)

                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=self.cladding_width / 2 + 1, l_max=25, waveguide_type=self)

                    @fpt.const_property
                    def theoretical_parameters(self):
                        return fpt.sim.TheoreticalParameters(wl=SWG_C_EXPANDED_SIM_WL, n_eff=SWG_C_EXPANDED_SIM_NEFF, loss=SWG_C_EXPANDED_SIM_LOSS)
                        raise NotImplementedError("No theoretical parameters for this updated waveguide-type")

                return EXPANDED()



if __name__ == "__main__":
    from pathlib import Path
    from fnpcell import all as fp
    from fpdk.technology import get_technology

    TECH = get_technology()
    folder = Path(__file__).parent
    generated_folder = folder / "generated"
    csv_file = generated_folder / "wg.csv"
    # ================================

    fp.util.generate_csv_from_waveguides(csv_file=csv_file, waveguides=TECH.WG, overwrite=True)
