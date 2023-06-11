import math
from dataclasses import dataclass
from typing import Tuple
from gpdk.technology import get_technology, WG
from fnpcell import all as fp
from gpdk import all as pdk

@dataclass(eq=False)
class fpPinPort(fp.PCell):

    height: float = fp.PositiveFloatParam(default=10)
    width: float = fp.PositiveFloatParam(default=50)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=("op_0", "ep_0"))


    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        mmi = pdk.Mmi()

        insts += mmi


        rec = fp.el.Rect(height=self.height, width=self.width, center=(0, 0), layer=TECH.LAYER.FWG_COR)
        # elems += rec

        # ports += fp.Port(name=self.port_names[0], position=(-self.width/2, 0),
        #                  waveguide_type=TECH.WG.FWG.C.WIRE.updated(core_layout_width=self.height), orientation=-math.pi)
        ports += fp.Port(
            name="test",
            at=mmi["op_0"],
            waveguide_type=TECH.WG.FWG.C.WIRE,
            orientation=-math.pi
        )
        # ports += fp.Pin(name=self.port_names[1], position=(self.width/2, 0), metal_line_type=TECH.METAL.M1.W10, orientation=math.pi)



        return insts, elems, ports



if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += fpPinPort()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
    print(fpPinPort().ports)