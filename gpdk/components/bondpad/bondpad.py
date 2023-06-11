import math
from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class BondPad(fp.PCell):
    """
    Attributes:
        pad_width: defaults to 75, width of the bondpad
        pad_height: defaults to 75, height of the bondpad
        port_names: defaults to ["ep_0", "ep_1"]

    Examples:
    ```python
    bondpad = BondPad(pad_width=75, pad_height=75)
    fp.plot(bondpad)
    ```
    ![BondPad](images/bondpad.png)
    """

    pad_width: float = fp.PositiveFloatParam(default=75)
    pad_height: float = fp.PositiveFloatParam(default=75)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["ep_0", "ep_1"])

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off

        pad = fp.el.Rect(width=self.pad_width, height=self.pad_height, center=(0, 0), layer=TECH.LAYER.MT_DRW)
        elems += pad
        pad_open = fp.el.Rect(width=self.pad_width - 5, height=self.pad_height - 5, center=(0, 0), layer=TECH.LAYER.PASS_MT)
        elems += pad_open

        ports += fp.Pin(name=self.port_names[0], position=(0, 0), orientation=-math.pi/2, shape=pad.shape, metal_line_type=TECH.METAL.MT.W20)
        ports += fp.Pin(name=self.port_names[1], position=(0, 0), orientation=-math.pi/2,shape=pad_open.shape, metal_line_type=TECH.METAL.PASS_MT.W20)
        print(pad.shape.shape_points)

        # fmt: on
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
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += BondPad()
    # library += BondPad75()
    # library += BondPad100()
    # library += BondPad(pad_width=75, pad_height=75)
    # library += BondPad(pad_width=80, pad_height=60, transform=fp.translate(100, 0))
    # library += BondPad(pad_width=100, pad_height=100, transform=fp.translate(200, 0))

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
