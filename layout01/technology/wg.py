from dataclasses import dataclass

from fnpcell.pdk.technology import all as fpt
from gpdk.technology.tech import TECH as GPDK_TECH

FWG_core_width = 0.45


class WG(GPDK_TECH.WG):
    class FWG(GPDK_TECH.WG.FWG):
        class C(GPDK_TECH.WG.FWG.C):
            @fpt.const_property
            def BEND_TEST(self):
                return GPDK_TECH.WG.FWG.C.WIRE.BEND_CIRCULAR

            @fpt.staticconst
            def WIRE():
                @fpt.hash_code
                @dataclass(frozen=True)
                class WIRE_NEW(__class__, type(GPDK_TECH.WG.FWG.C.WIRE)):
                    core_design_width: float = FWG_core_width
                    cladding_design_width: float = 4.45

                    @fpt.classconst
                    @classmethod
                    def core_bias(cls):
                        return fpt.CDBiasLinear(0.1)

                    @fpt.const_property
                    def BEND_TEST2(self):
                        return GPDK_TECH.WG.FWG.C.WIRE.BEND_CIRCULAR

                return WIRE_NEW()


if __name__ == "__main__":
    from pathlib import Path
    from fnpcell import all as fp
    from layout01.technology import get_technology

    TECH = get_technology()
    folder = Path(__file__).parent
    generated_folder = folder / "generated"
    csv_file = generated_folder / "wg.csv"
    # ================================

    fp.util.generate_csv_from_waveguides(csv_file=csv_file, waveguides=TECH.WG, overwrite=True)
