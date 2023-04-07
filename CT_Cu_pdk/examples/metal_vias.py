from dataclasses import dataclass
from fnpcell import all as fp
from CT_Cu_pdk import all as pdk
from CT_Cu_pdk.technology import get_technology


@dataclass(eq=False)
class heater(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        box = fp.el.Line(length=10, stroke_width=10, layer=TECH.LAYER.M1, anchor=fp.Anchor.CENTER)
        elems += box
        ports += fp.Pin(name="ep_0", position=(0, 0), orientation=90, shape=box.shape,
                        metal_line_type=TECH.METAL.M1.W10)

        return insts, elems, ports


@dataclass(eq=False)
class test_vias(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        heater1 = heater()
        heater2 = heater().translated(tx=100, ty=0)

        link = fp.Linked(
            metal_line_type=TECH.METAL.M2.W10,
            metal_min_distance=10,
            links=[
                heater1["ep_0"].with_orientation(degrees=90) >> heater2["ep_0"].with_orientation(degrees=90)
            ],
            auto_vias=TECH.AUTO_VIAS.DEFAULT,
            ports=[],

        )
        insts += link

        elems += heater1, heater2

        return insts, elems, ports


#

if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += test_vias()
    # library += SiHeater(length=50, waveguide_type=TECH.WG.FWG.C.WIRE)

    # fmt: on
    # =============================================================
    fp.plot(library)
