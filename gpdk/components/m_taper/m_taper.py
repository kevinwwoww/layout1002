from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class MTaper(fp.PCell):
    """
    Attributes:
        initial_width: defaults to 21
        final_width: defaults to 75
        final_offset: defaults to 0, offset of the far-end, positive for left, negative for right
        length: defaults to 20

    Examples:
    ```python
    TECH = get_technology()
        m_taper = MTaper(final_offset=27)
    fp.plot(m_taper)
    ```
    ![MTaper](images/M_Taper.png)
    """

    initial_width: float = fp.PositiveFloatParam(default=21)
    final_width: float = fp.PositiveFloatParam(default=75)
    final_offset: float = fp.FloatParam(default=0)
    length: float = fp.PositiveFloatParam(default=20)

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off

        taper = fp.el.Line(stroke_width=self.initial_width, final_stroke_width=self.final_width, final_stroke_offset=self.final_offset, length=self.length, layer=TECH.LAYER.MT_DRW)
        elems += taper

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    # library += MTaper(final_offset=27)
    library += MTaper()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
