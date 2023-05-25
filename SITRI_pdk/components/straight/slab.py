from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from fnpcell import all as fp
from fnpcell.interfaces import angle_between, distance_between
from SITRI_pdk.technology import get_technology, WG


@dataclass(eq=False)
class Slab(fp.IWaveguideLike, fp.PCell):
    """
    Attributes:
        length: length of straight
        waveguide_type: type of waveguide
        anchor: defaults to `Anchor.START`, origin of the straight(START at origin, CENTER at origin or End at origin)
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
        # straight = Straight(name="s", length=10, waveguide_type=TECH.WG.RIB.C.WIRE)
    fp.plot(straight)
    ```
    ![Straight](images/straight.png)
    """

    Length: float = fp.FloatParam(default=5.0, min=0)
    Width: float = fp.FloatParam(default=1.0, min=0)
    RibInSlab: float = fp.FloatParam(default=5.0, min=0)
    waveguide_type: WG.SLAB.C = fp.WaveguideTypeParam()
    anchor: fp.Anchor = fp.AnchorParam(default=fp.Anchor.START)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=("op_0", "op_1"))

    def _default_waveguide_type(self):
        return get_technology().WG.SLAB.C.WIRE.updated(wg_design_width=self.Width, wg_slab_design_width=self.RibInSlab * 2)

    @cached_property
    def raw_curve(self):
        return fp.g.Line(
            length=self.Length,
            anchor=self.anchor,
        )


    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        wg = self.waveguide_type(curve=self.raw_curve).with_ports(self.port_names)
        insts += wg
        ports += wg.ports
        return insts, elems, ports


def StraightBetween(
        *,
        start: fp.Point2D = (0, 0),
        end: fp.Point2D,
        waveguide_type: fp.IWaveguideType,
        port_names: fp.IPortOptions = ("op_0", "op_1"),
):
    length = distance_between(end, start)
    orientation = angle_between(end, start)
    straight = Slab(Length=length, waveguide_type=waveguide_type, port_names=port_names).rotated(
        radians=orientation).translated(*start)
    return straight


if __name__ == "__main__":
    from SITRI_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += Slab()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
