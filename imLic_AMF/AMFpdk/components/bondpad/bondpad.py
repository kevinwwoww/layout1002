import math
from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from AMFpdk.technology import get_technology

@dataclass(eq=False)
class BondPad(fp.PCell):

    pad_width: float = fp.PositiveFloatParam(default=50)
    pad_height: float = fp.PositiveFloatParam(default=50)
    port_names: fp.IPortOption = fp.PortOptionsParam(count=2, default=["ep_0", "ep_1"])

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()

        pad = fp.el.Rect(width=self.pad_width, height=self.pad_height, center=(0, 0), layer=TECH.LAYER.MT2)
        elems += pad
        pad_open = fp.el.Rect(width=self.pad_width - 2, height=self.pad_height - 2, center=(0, 0), layer=TECH.LAYER.PAD)
        elems += pad_open

        ports += fp.Pin(name=self.port_names[0], position=(0, 0), orientation=-math.pi/2, shape=pad.shape, metal_line_type=TECH.METAL.MT2.W20)
        ports += fp.Pin(name=self.port_names[1], position=(0, 0), orientation=-math.pi/2, shape=pad.shape, metal_line_type=TECH.METAL.PAD.W20)

        return insts, elems, ports

@dataclass(eq=False)
class BondPad75(BondPad):
    pad_width: float = fp.PositiveFloatParam(default=75, locked=True)
    pad_height: float = fp.PositiveFloatParam(default=75, locked=True)


@dataclass(eq=False)
class BondPad100(BondPad):
    pad_width: float = fp.PositiveFloatParam(default=100, locked=True)
    pad_height: float = fp.PositiveFloatParam(default=100, locked=True)


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file
    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology

    library += BondPad()

    fp.export_gds(library, file=gds_file)