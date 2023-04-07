from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk.components.straight.straight import Straight
from AMFpdk.components.taper.taper_linear import TaperLinear
from AMFpdk.technology import get_technology
from AMFpdk.technology.interfaces import CoreWaveguideType


@dataclass(eq=False)
class Cwg(fp.PCell):
    mid_wav_core_width: float = fp.PositiveFloatParam(default=5)
    wav_core_width: float = fp.PositiveFloatParam(default=1)
    # end_core_width=fp.PositiveFloatParam(default=0.45)
    n_inputs: int = fp.PositiveIntParam(default=1)
    n_outputs: int = fp.PositiveIntParam(default=2)
    length: float = fp.PositiveFloatParam(default=25)
    transition_length: float = fp.PositiveFloatParam(default=5)
    trace_spacing: float = fp.PositiveFloatParam(default=2)
    waveguide_type: CoreWaveguideType = fp.WaveguideTypeParam(type=CoreWaveguideType)

    def _default_waveguide_type(self):
        return get_technology().WG.RIB.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        mid_wav_core_width = self.mid_wav_core_width
        wav_core_width = self.wav_core_width
        n_inputs = self.n_inputs
        n_outputs = self.n_outputs
        length = self.length
        transition_length = self.transition_length
        trace_spacing = self.trace_spacing
        waveguide_type = self.waveguide_type

        center_type = waveguide_type.updated(wg_layout_width=mid_wav_core_width)
        center = Straight(length=length, waveguide_type=center_type, anchor=fp.Anchor.CENTER)
        insts += center
        center = Straight(length=length, waveguide_type=center_type, anchor=fp.Anchor.CENTER).rotated(degrees=90)
        insts += center

        wide_type = waveguide_type.updated(wg_layout_width=(wav_core_width))
        narrow_type = waveguide_type.updated(wg_layout_width=wav_core_width)
        taper_left = TaperLinear(length=transition_length, left_type=narrow_type, right_type=wide_type,
                                 anchor=fp.Anchor.END)
        taper_bottom = TaperLinear(length=transition_length, left_type=narrow_type, right_type=wide_type,
                                 anchor=fp.Anchor.END).rotated(degrees=90)
        taper_right = TaperLinear(length=transition_length, left_type=wide_type, right_type=narrow_type,
                                  anchor=fp.Anchor.START)
        taper_top = TaperLinear(length=transition_length, left_type=narrow_type, right_type=wide_type,
                                 anchor=fp.Anchor.END).rotated(degrees=90)

        taper_left_inst = taper_left.translated(-length/2,0)
        insts += taper_left_inst
        ports += taper_left_inst["op_0"].with_name(f"op_{0}")

        taper_bottom_inst = taper_bottom.translated(0, -length/2)
        insts += taper_bottom_inst
        ports += taper_bottom_inst["op_0"].with_name(f"op_{1}")

        taper_right_inst = taper_right.translated(length/2, 0)
        insts += taper_right_inst
        ports += taper_right_inst["op_1"].with_name(f"op_{2}")

        taper_top_inst = taper_top.translated(0, length/2+transition_length)
        insts += taper_top_inst
        ports += taper_top_inst["op_1"].with_name(f"op_{3}")


        return insts, elems, ports


# @dataclass(eq=False)
# class MMI1x2(MMI, locked=True):
#     n_inputs: int = fp.PositiveIntParam(default=1)
#     n_outputs: int = fp.PositiveIntParam(default=2)


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    library += Cwg(name="s", n_inputs=1)
    # library += MMI1x2()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
