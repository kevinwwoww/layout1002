import math
from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.components.bondpad.bondpad import BondPad
from gpdk.components.m_taper.m_taper import MTaper
from gpdk.technology import get_technology


@dataclass(eq=False)
class BondPadTapered(fp.PCell):
    """
    Attributes:
        pad_width: defaults to 75, width of the bondpad
        pad_height: defaults to 75, height of the bondpad
        taper_width: defaults to 20, width of the far-end of the taper part
        taper_offset: defaults to 0, offset of the far-end, positive for left, negative for right. (base direction is from bondpad to taper)
        taper_width: defaults to 20, length of the taper part
        port_names: defaults to ["ep_0", "ep_1"]

    Examples:
    ```python
    bondpad = BondPadTapered(pad_width=75, pad_height=75)
    fp.plot(bondpad)
    ```
    ![BondPadTapered](images/bondpad_tapered.png)
    """

    pad_width: float = fp.PositiveFloatParam(default=75)
    pad_height: float = fp.PositiveFloatParam(default=75)
    taper_width: float = fp.PositiveFloatParam(default=20)
    taper_offset: float = fp.FloatParam(default=0)
    taper_length: float = fp.PositiveFloatParam(default=20)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["ep_0", "ep_1"])

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off

        pad_width = self.pad_width
        pad_height = self.pad_height
        taper_width = self.taper_width
        taper_length =self.taper_length
        taper_offset = self.taper_offset
        port_names = self.port_names
        bond_pad = BondPad(pad_width=pad_width, pad_height=pad_height, port_names=[None, "ep_1"])
        insts += bond_pad
        (_, y_min), (_, _) = fp.get_bounding_box(bond_pad)
        m_taper = MTaper(initial_width=pad_width, final_width=taper_width, final_offset=taper_offset, length=taper_length, transform=fp.rotate(degrees=-90).translate(0, y_min))
        insts += m_taper
        ports += fp.Pin(name=port_names[0], position=(0, y_min), orientation=-math.pi/2, shape=fp.g.Rect(width=0.1, height=0.1, center=(0, 0)).translated(0, y_min), metal_line_type=TECH.METAL.MT.W20)  #layers=[TECH.LAYER.MT_DRW]
        ports += bond_pad["ep_1"].with_name(port_names[1])

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += BondPadTapered()
    # library += BondPadTapered(pad_width=75, pad_height=75)
    # library += BondPadTapered(pad_width=80, pad_height=60, transform=fp.translate(100, 0))
    # library += BondPadTapered(pad_width=100, pad_height=100, transform=fp.translate(200, 0))

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
