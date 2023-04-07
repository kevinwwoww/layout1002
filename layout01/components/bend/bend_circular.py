from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from fnpcell import all as fp
from layout01.technology import get_technology


@dataclass(eq=False)
class BendCircular(fp.IWaveguideLike, fp.PCell):
    degrees: float = fp.DegreeParam(default=90, min=0, max=90, doc="Bend angle in degrees")
    radius: float = fp.PositiveFloatParam(doc="Bend radius")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

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


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    top_cell_name = "sss"

    # library += fp.Device(content=[BendCircular(name="s", radius=5, waveguide_type=TECH.WG.FWG.C.WIRE)], ports=[])
    # library += BendCircular(radius=10, waveguide_type=TECH.WG.FWG.C.WIRE).translated(0, 15).with_name(top_cell_name)
    library += BendCircular(name="bend1", radius=5,
                            waveguide_type=TECH.WG.FWG.C.WIRE)
    library += BendCircular(name="bend2", radius=10, degrees=30,
                            waveguide_type=TECH.WG.FWG.C.WIRE, transform=fp.translate(0, 5))
    library += BendCircular(name="bend3", radius=10, degrees=60,
                            waveguide_type=TECH.WG.FWG.C.WIRE).translated(5, 5)
    library += BendCircular(name="bend4", radius=10, degrees=90,
                            waveguide_type=TECH.WG.FWG.C.WIRE, transform=fp.translate(0,
                                                                                      5)).translated(5, 5)

    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.export_spc(library, file=gds_file.with_suffix(".spc"))
    fp.generate_svrf(top_cell_name=top_cell_name, gds_path=gds_file, file=gds_file.with_suffix(".svrf"))
    #  fp.plot(library)
