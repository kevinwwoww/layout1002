from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk.components.straight.straight import Straight
from gpdk.technology import get_technology


@dataclass(eq=False)
class SiHeater(fp.PCell):
    """
    Attributes:
        length: defaults to 0.5, length of the heater
        half_metal_width: defaults to 1.0, Half width of M1 layer
        waveguide_type: type of waveguide
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
        heater = SiHeater(length=50, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(heater)
    ```
    ![SiHeater](images/si_heater.png)
    """

    length: float = fp.PositiveFloatParam(default=0.5, doc="Length of the heater")
    half_metal_width: float = fp.PositiveFloatParam(default=1.0, doc="Half width of M1 layer")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off

        wg = Straight(name="wg", length=self.length, waveguide_type=self.waveguide_type)
        metal = fp.el.Line(length=self.length, stroke_width=self.half_metal_width * 2, layer=TECH.LAYER.M1_DRW)
        insts += wg
        ports += wg["op_0"].with_name(self.port_names[0])
        ports += wg["op_1"].with_name(self.port_names[1])
        elems += metal

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += SiHeater()
    # library += SiHeater(length=50, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
