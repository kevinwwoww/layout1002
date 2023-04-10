from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk.technology import get_technology

@dataclass(eq=False)
class MTaper(fp.PCell):
    """
    metal taper
    """

    initial_width: float = fp.PositiveFloatParam(default=21)
    final_width: float = fp.PositiveFloatParam(default=75)
    final_offset: float = fp.FloatParam(default=0)
    length: float = fp.PositiveFloatParam(default=20)

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        initial_width = self.initial_width
        final_width = self.final_width
        final_offset = self.final_offset
        length = self.length

        taper = fp.el.Line(stroke_width=initial_width, final_stroke_width=final_width, final_stroke_offset=final_offset, length=length, layer=TECH.LAYER.MT1)
        elems += taper

        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file
    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += MTaper()

    fp.export_gds(library, file=gds_file)
