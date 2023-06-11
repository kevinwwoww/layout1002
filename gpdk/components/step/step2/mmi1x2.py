from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk.components.step.step1.straight import Straight
from gpdk.components.step.step1.taper_linear import TaperLinear
from gpdk.technology import get_technology
from gpdk.technology.interfaces import CoreCladdingWaveguideType


@dataclass(eq=False)
class MMI1x2(fp.PCell):
    """
    Attributes:
        mid_wav_core_width: defaults to 5
        wav_core_width: defaults to 1
        length: defaults to 25
        transition_length: defaults to 5
        trace_spacing: defaults to 2
        waveguide_type: type of waveguide

    Examples:
    ```python
    TECH = get_technology()
        mmi = Mmi(waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(mmi)
    ```
    ![Mmi](images/mmi.png)
    """

    mid_wav_core_width: float = fp.PositiveFloatParam(default=5)
    wav_core_width: float = fp.PositiveFloatParam(default=1.5)
    length: float = fp.PositiveFloatParam(default=10)
    transition_length: float = fp.PositiveFloatParam(default=5)
    trace_spacing: float = fp.PositiveFloatParam(default=1)
    waveguide_type: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        # fmt: off
        mid_wav_core_width = self.mid_wav_core_width
        wav_core_width=self.wav_core_width
        length = self.length
        transition_length = self.transition_length
        trace_spacing = self.trace_spacing
        waveguide_type = self.waveguide_type

        center_force_cladding_width = mid_wav_core_width+waveguide_type.cladding_width
        center_type = waveguide_type.updated(core_layout_width=mid_wav_core_width, cladding_layout_width=center_force_cladding_width)
        center = Straight(length=length, waveguide_type=center_type, anchor=fp.Anchor.START)
        insts += center

        wide_type = waveguide_type.updated(core_layout_width=wav_core_width, cladding_layout_width=waveguide_type.cladding_width + wav_core_width)
        narrow_type = waveguide_type
        taper_left = TaperLinear(length=transition_length, left_type=narrow_type, right_type=wide_type, anchor=fp.Anchor.END)
        taper_right = TaperLinear(length=transition_length, left_type=wide_type, right_type=narrow_type, anchor=fp.Anchor.START)


        taper_left_inst = taper_left.translated(0, 0)
        insts += taper_left_inst
        ports += taper_left_inst["op_0"].with_name("op_0")

        taper_right_inst1 = taper_right.translated(length, -(wav_core_width+trace_spacing)/2)
        insts += taper_right_inst1
        ports += taper_right_inst1["op_1"].with_name(f"op_1")
        taper_right_inst2 = taper_right.translated(length, (wav_core_width+trace_spacing)/2)
        insts += taper_right_inst2
        ports += taper_right_inst2["op_1"].with_name(f"op_2")

        # fmt: on
        return insts, elems, ports




if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += MMI1x2()


    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
