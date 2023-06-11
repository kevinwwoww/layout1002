import math
from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class ContactHole(fp.PCell):
    """
    Attributes:
        num_sides: Number of sides of the polygon used for the contact hole
        top_width: Width of the top layer (2 * inner radius of the polygon)
        tin_width: Width of the TiN layer
        bottom_width: Width of the bottom layer (2 * inner radius of the polygon)
        via_width: Width of the via layer (2 * inner radius of the polygon)
        port_names: defaults to ["M1"]

    Examples:
    ```python
    contact_hole = ContactHole(name="d", num_sides=4, top_width=2, bottom_width=1.6, via_width=0.4)
    fp.plot(contact_hole)
    ```
    ![ContactHole](images/contact_hole.png)
    """

    num_sides: int = fp.IntParam(default=8, min=3, doc="Number of sides of the polygon used for the contact hole")
    top_width: float = fp.PositiveFloatParam(default=1.0, doc="Width of the top layer (2 * inner radius of the polygon)")
    bottom_width: float = fp.PositiveFloatParam(default=0.8, doc="Width of the bottom layer (2 * inner radius of the polygon)")
    via_width: float = fp.PositiveFloatParam(default=0.2, doc="Width of the via layer (2 * inner radius of the polygon)")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=1, default=["M1"])

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off

        num_sides = self.num_sides
        angle = math.pi / num_sides
        tan = math.tan(angle)
        top_side_length = self.top_width * tan
        bottom_side_length = self.bottom_width * tan
        via_side_length = self.via_width * tan

        elems += fp.el.RegularPolygon(sides=num_sides, side_length=top_side_length, layer=TECH.LAYER.M1_DRW)
        via = fp.el.RegularPolygon(sides=num_sides, side_length=via_side_length, layer=TECH.LAYER.VIA1_DRW)
        elems += via
        elems += fp.el.RegularPolygon(sides=num_sides, side_length=bottom_side_length, layer=TECH.LAYER.FWG_COR)
        ports += fp.Pin(name=self.port_names[0], position=(0, 0),orientation=-math.pi/2, shape=via.shape, metal_line_type=TECH.METAL.M1.W20)

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += ContactHole()
    # library += ContactHole(name="d", num_sides=4, top_width=2, bottom_width=1.6, via_width=0.4)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
