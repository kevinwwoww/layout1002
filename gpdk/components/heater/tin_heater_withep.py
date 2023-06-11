import math
from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.components.straight.straight import Straight
from gpdk.technology import get_technology


@dataclass(eq=False)
class TiNHeaterwithep(fp.PCell):
    """
    Attributes:
        waveguide_length: defaults to 25, Waveguide length
        tin_length: defaults to 15, TiN length
        tin_width: defaults to 2.0, TiN width
        tin_box_size: defaults to 8, TiN box edge size
        metal_box_size: defaults to 10, Metal box edge size
        contact_box_size: defaults to 6, Contact box edge size
        waveguide_type: type of waveguide
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
        heater = TiNHeater(waveguide_length=50, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(heater)
    ```
    ![TiNHeater](images/tin_heater.png)
    """

    waveguide_length: float = fp.PositiveFloatParam(default=25, doc="Waveguide length")
    tin_length: float = fp.PositiveFloatParam(default=15, doc="TiN length")
    tin_width: float = fp.PositiveFloatParam(default=2.0, doc="TiN width")
    tin_box_size: float = fp.PositiveFloatParam(default=8, doc="TiN box edge size")
    metal_box_size: float = fp.PositiveFloatParam(default=10, doc="Metal box edge size")
    contact_box_size: float = fp.PositiveFloatParam(default=6, doc="Contact box edge size")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4, default=["op_0", "op_1", "ep_0", "ep_1"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off
        waveguide_length = self.waveguide_length
        tin_length = self.tin_length
        tin_width = self.tin_width
        tin_box_size = self.tin_box_size
        metal_box_size = self.metal_box_size
        contact_box_size = self.contact_box_size
        waveguide_type = self.waveguide_type
        port_names = self.port_names

        ct_box_size = 0.25
        min_ct_spacing = 0.35
        n = math.floor(contact_box_size / min_ct_spacing)
        ct_spacing = contact_box_size / n
        tx = tin_length / 2
        t = (ct_spacing - ct_box_size) / 2

        ct_box = fp.el.Line(length=ct_box_size, stroke_width=ct_box_size, layer=TECH.LAYER.CONT_DRW, transform=fp.translate(t, t))
        ct_box = fp.Composite(ct_box).with_ports().with_name("ct").new_array(cols=n, col_width=ct_spacing, rows=n, row_height=ct_spacing)

        insts += ct_box.translated(-contact_box_size / 2 - tx, -contact_box_size / 2)
        insts += ct_box.translated(-contact_box_size / 2 + tx, -contact_box_size / 2)

        wg = Straight(name="wg", length=waveguide_length, waveguide_type=waveguide_type, transform=fp.translate(-waveguide_length / 2, 0))
        insts += wg
        ports += wg["op_0"].with_name(port_names[0])
        ports += wg["op_1"].with_name(port_names[1])

        tin = fp.el.Line(length=tin_length, stroke_width=tin_width, layer=TECH.LAYER.TIN_DRW, anchor=fp.Anchor.CENTER)
        elems += tin



        m1_box = fp.el.Rect(width=metal_box_size, height=metal_box_size, center=(0, 0), layer=TECH.LAYER.M1_DRW)
        elems += m1_box.translated(-tx, 0)
        elems += m1_box.translated(tx, 0)

        tin_box = fp.el.Rect(width=tin_box_size, height=tin_box_size, center=(0, 0), layer=TECH.LAYER.TIN_DRW)
        tin_box_left = tin_box.translated(-tx, 0)
        elems += tin_box_left
        tin_box_right = tin_box.translated(tx, 0)
        elems += tin_box_right
        ports += fp.Pin(name=port_names[3], position=(tx, 0), orientation=-math.pi / 2, shape=tin_box_right.shape, metal_line_type=TECH.METAL.MT.W10)
        ports += fp.Pin(name=port_names[2], position=(-tx, 0), orientation=-math.pi / 2, shape=tin_box_left.shape, metal_line_type=TECH.METAL.MT.W10)

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off


    library += TiNHeaterwithep()
    # library += TiNHeater(waveguide_length=50, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
    print(TiNHeaterwithep.port_names)