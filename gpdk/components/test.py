import math
from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.components.heater.si_heater import SiHeater
from gpdk.technology import WG, get_technology

@dataclass(eq=False)
class updated(fp.PCell):

    length: float = fp.PositiveFloatParam(default=10)
    length_is_10: bool = fp.BooleanParam(default=True)
    heater: fp.IDevice = fp.DeviceParam()
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_heater(self):
        return SiHeater(length=20)

    def build(self):
        insts, elems, ports = super().build()

        length = self.length
        heater = self.heater
        length_is_10 = self.length_is_10

        heater1 = self.heater.updated(length=100)

        # fp.create_links(link_type=, bend_factory=, )

        insts += heater1

        print(heater1)

        return insts, elems, ports

if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += updated()

    # fmt: on
    # =============================================================
    # fp.export_gds(library, file=gds_file)
    # fp.plot(library)



