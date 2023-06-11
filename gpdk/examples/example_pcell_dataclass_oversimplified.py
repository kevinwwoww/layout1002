# type: ignore
#### import necessary modules ####
from functools import cached_property

from fnpcell import all as fp
from gpdk.technology import get_technology  # get TECH definition

#### finish import ####

#### define pcell, use BendCircular for example ####
#### WARNING: simplified version of pcell class definition is not good for typing checker


class BendCircular(fp.IWaveguideLike, fp.PCell, band="C"):
    degrees = fp.DegreeParam(default=90, min=0, max=90, doc="Bend angle in degrees")
    radius = fp.PositiveFloatParam(doc="Bend radius")
    waveguide_type = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    @cached_property
    def raw_curve(self):
        return fp.g.EllipticalArc(radius=self.radius, final_degrees=self.degrees)

    def build(self):
        insts, elems, ports = super().build()
        wg = self.waveguide_type(curve=self.raw_curve).with_ports(self.port_names)
        insts += wg
        ports += wg.ports
        return insts, elems, ports


class BendCircular90(BendCircular, band="C"):
    degrees = fp.DegreeParam(locked=True, default=90, min=0, max=90, doc="Bend angle in degrees")


if __name__ == "__main__":
    # fixed template start
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    # =============================================================
    # fmt: off
    # fixed template end
    # custom region start
    r0 = BendCircular(degrees=60, radius=10, waveguide_type=TECH.WG.FWG.C.WIRE, port_names=("op_0", "op_1"))
    library += r0
    r1 = BendCircular(degrees=45, radius=10, waveguide_type=TECH.WG.MWG.C.WIRE).translated(20, 0)
    library += r1
    r2 = BendCircular90(radius=10, waveguide_type=TECH.WG.SWG.C.WIRE).translated(50, 0)
    library += r2
    # custom region end

    # fixed template start
    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
    # fixed template end
