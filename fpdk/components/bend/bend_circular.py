from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Tuple

from fnpcell import all as fp
from fpdk.technology import get_technology


@dataclass(eq=False)
class BendCircular(fp.IWaveguideLike, fp.PCell):
    """
    Attributes:
        degrees: central angle of the bend, in degrees
        radius: raidus of the bend
        waveguide_type: type of waveguide of the bend
        port_names: defaults to ["op_0", "op_1"]

    Examples:
    ```python
    TECH = get_technology()
        bend = BendCircular(name="s", radius=5, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(bend)
    ```
    ![BendCircular](images/bend_circular.png)
    """
    degrees: float = fp.DegreeParam(default=90, min=-180, max=180, doc="Bend angle in degrees")
    radius: float = fp.PositiveFloatParam(default=10, doc="Bend radius")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def __post_pcell_init__(self):
        assert fp.is_nonzero(self.degrees)

    @cached_property
    def raw_curve(self):
        return fp.g.EllipticalArc(
            radius=self.radius,
            final_degrees=self.degrees,
        )

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        wg = self.waveguide_type(curve=self.raw_curve).with_ports(self.port_names)
        insts += wg
        ports += wg.ports
        return insts, elems, ports


@dataclass(eq=False)
class BendCircular90(BendCircular):
    degrees: float = fp.DegreeParam(default=90, locked=True)
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(locked=True)

    @fp.cache()
    def sim_model(self, env: fp.ISimEnv):
        return fp.sim.ExternalFileModel(Path(f"{type(self).__name__}_radius={self.radius}").with_suffix(".dat"))


@dataclass(eq=False)
class BendCircular90_FWG_C_WIRE(BendCircular90, locked=True):
    radius: float = fp.PositiveFloatParam(default=3.225, doc="Bend radius")

    @fp.cache()
    def sim_model(self, env: fp.ISimEnv):
        return fp.sim.ExternalFileModel(Path("BendCircular90_radius=10").with_suffix(".dat"))


@dataclass(eq=False)
class BendCircular90_FWG_C_EXPANDED(BendCircular, locked=True):
    radius: float = fp.PositiveFloatParam(default=3.4, doc="Bend radius")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam()

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.EXPANDED

    @fp.cache()
    def sim_model(self, env: fp.ISimEnv):

        file_path = Path("BendCircular90_radius=10").with_suffix(".dat")

        return fp.sim.ExternalFileModel(file_path)

@dataclass(eq=False)
class BendCircular_FWG_C_WIRE(BendCircular, locked=True):

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

@dataclass(eq=False)
class BendCircular_FWG_C_EXPANDED(BendCircular):

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.EXPANDED

@dataclass(eq=False)
class BendCircular_SWG_C_WIRE(BendCircular):

    def _default_waveguide_type(self):
        return get_technology().WG.SWG.C.WIRE

@dataclass(eq=False)
class BendCircular_SWG_C_EXPANDED(BendCircular):

    def _default_waveguide_type(self):
        return get_technology().WG.SWG.C.EXPANDED

if __name__ == "__main__":
    from fpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    # library += BendCircular(name="s", radius=15, waveguide_type=TECH.WG.FWG.C.WIRE)
    # library += BendCircular90()
    # library += BendCircular(name="d", radius=10, waveguide_type=TECH.WG.FWG.C.WIRE).translated(0, 15)
    # library += BendCircular()
    library += BendCircular_FWG_C_WIRE()
    # print(BendCircular().cell.polygon_set(layer=TECH.LAYER.FWG_COR,union=False))


    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
