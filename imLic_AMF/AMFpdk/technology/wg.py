from dataclasses import dataclass

from fnpcell.pdk.technology import all as fpt
from AMFpdk.technology.interfaces import CoreWaveguideType, SlabWaveguideType
from AMFpdk.technology.waveguide_factory import StraightFactory, CircularBendFactory, EulerBendFactory

# from  gpdk_AMF.technology.waveguide_factory import CircularBendFactory, EulerBendFactory, StraightFactory

RIB_WIDTH = 0.5
GRAT_WIDTH = 1.0
SLAB_WIDTH = 10.0

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
class RIB_C(CoreWaveguideType):
    @fpt.const_property
    def wg_bias(self):
        return fpt.CDBiasLinear(0.1)

    @fpt.const_property
    def band(self):
        from AMFpdk.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def wg_layer(self):
        from AMFpdk.technology import get_technology

        return get_technology().LAYER.RIB

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class GRAT_C(CoreWaveguideType):
    @fpt.const_property
    def wg_bias(self):
        return fpt.CDBiasLinear(0.1)

    @fpt.const_property
    def band(self):
        from AMFpdk.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def wg_layer(self):
        from AMFpdk.technology import get_technology

        return get_technology().LAYER.GRAT

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class SLAB_C(CoreWaveguideType):
    @fpt.const_property
    def wg_bias(self):
        return fpt.CDBiasLinear(0.1)

    @fpt.const_property
    def band(self):
        from AMFpdk.technology import get_technology

        return get_technology().BAND.C

    @fpt.const_property
    def wg_layer(self):
        from AMFpdk.technology import get_technology

        return get_technology().LAYER.SLAB

    @fpt.const_property
    def straight_factory(self):
        return StraightFactory()


@fpt.hash_code
@dataclass(frozen=True)
class RIBnSLAB_C(SlabWaveguideType):
    @fpt.const_property
    def wg_slab_bias(self):
        return fpt.CDBiasLinear(0.1)

    @fpt.const_property
    def wg_rib_bias(self):
        return fpt.CDBiasLinear(0)

    @fpt.const_property
    def band(self):
        from AMFpdk.technology import get_technology

        return get_technology().BAND.C

    def wg_slab_layer(self):
        from AMFpdk.technology import get_technology
        return get_technology().LAYER.SLAB

    def wg_layer(self):
        from AMFpdk.technology import get_technology
        return get_technology().LAYER.RIB


class WG:
    class RIB:
        class C(RIB_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    wg_design_width: float = RIB_WIDTH


                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_EULER

                    #
                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=self.wg_width, waveguide_type=self)

                    #
                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=self.wg_width+10, l_max=5, waveguide_type=self)

                    @fpt.const_property
                    def theoretical_parameters(self):
                        if self == WG.RIB.C.WIRE:
                            return fpt.sim.TheoreticalParameters(wl=RIB_SIM_WL, n_eff=RIB_SIM_NEFF, loss=RIB_SIM_LOSS)
                        raise NotImplementedError("No theoretical parameters for this updated waveguide-type")

                return WIRE()

    class GRAT:
        class C(GRAT_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    wg_design_width: float = GRAT_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_CIRCULAR

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=self.wg_width, waveguide_type=self)

                    #
                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=self.wg_width, l_max=5, waveguide_type=self)

                    @fpt.const_property
                    def theoretical_parameters(self):
                        if self == WG.RIB.C.WIRE:
                            return fpt.sim.TheoreticalParameters(wl=GRAT_SIM_WL, n_eff=GRAT_SIM_NEFF,
                                                                 loss=GRAT_SIM_LOSS)
                        raise NotImplementedError("No theoretical parameters for this updated waveguide-type")

                return WIRE()

    class SLAB:
        class C(SLAB_C):
            @fpt.staticconst
            def WIRE():
                @dataclass(frozen=True)
                class WIRE(__class__):
                    wg_design_width: float = SLAB_WIDTH

                    @fpt.const_property
                    def bend_factory(self):
                        return self.BEND_CIRCULAR

                    @fpt.const_property
                    def BEND_CIRCULAR(self):
                        return CircularBendFactory(radius_eff=self.wg_width, waveguide_type=self)

                    #
                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=self.wg_width, l_max=5, waveguide_type=self)

                    @fpt.const_property
                    def theoretical_parameters(self):
                        if self == WG.RIB.C.WIRE:
                            return fpt.sim.TheoreticalParameters(wl=SLAB_SIM_WL, n_eff=SLAB_SIM_NEFF,
                                                                 loss=SLAB_SIM_LOSS)
                        raise NotImplementedError("No theoretical parameters for this updated waveguide-type")

                return WIRE()

    class RIBnSLAB:
        class C(RIBnSLAB_C):
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
                        return CircularBendFactory(radius_eff=self.wg_slab_width / 2 + 1, waveguide_type=self)

                    @fpt.const_property
                    def BEND_EULER(self):
                        return EulerBendFactory(radius_min=self.wg_slab_width / 2 + 1, l_max=5, waveguide_type=self)

                return WIRE()


if __name__ == "__main__":
    from pathlib import Path
    from fnpcell import all as fp
    from AMFpdk.technology import get_technology

    TECH = get_technology()
    folder = Path(__file__).parent
    generated_folder = folder / "generated_AMF"
    csv_file = generated_folder / "wg.csv"

    fp.util.generate_csv_from_waveguides(csv_file=csv_file, waveguides=TECH.WG, overwrite=True)
