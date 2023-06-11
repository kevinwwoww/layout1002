#### import necessary modules ####

from dataclasses import dataclass, field
from typing import cast
from functools import cached_property
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology  # get TECH definition
from gpdk.technology.interfaces import CoreCladdingWaveguideType

#### finish import ####

#### define pcell, use RingResonator for example ####


# the dataclass decorator is for IDE code complete
@dataclass(eq=False)
class PcellOrderTest(fp.PCell):
    #
    # define parameters
    #
    # parameter，with default value 5, will be validated in __post_pcell_init__
    parameterA: float = fp.FloatParam(default=5)
    parameterB: float = fp.FloatParam(default=10)
    parameter_waveguide: CoreCladdingWaveguideType = fp.WaveguideTypeParam(type=CoreCladdingWaveguideType)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4, default=["op_0", "op_1", "op_2", "op_3"])
    # finish parameter definition

    @cached_property
    def raw_curve(self):
        print("test")
        return fp.g.EllipticalArc(
            radius=10,
            final_degrees=90,
        )

    def _default_parameter_waveguide(self):
        print("assign default")
        return get_technology().WG.FWG.C.WIRE

    def __post_pcell_init__(self):
        print("__post_pcell_init__")
        assert self.parameterA > 0, "A must be a positive value"

    def __post_init__(self):
        print("__post_init__")
        assert self.parameterB > 0, "B must be a positive value"


    def build(self):
        # create insts,elems,ports, fixed template
        print("build method")
        insts, elems, ports = fp.InstanceSet(), fp.ElementSet(), fp.PortSet()

        return insts, elems, ports


if __name__ == "__main__":
    # fixed template start
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    library += PcellOrderTest()


