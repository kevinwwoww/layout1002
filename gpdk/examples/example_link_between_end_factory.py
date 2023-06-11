from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class LinkBetweenEndFactory(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        ec = pdk.Fixed_Edge_Coupler()
        pd = pdk.Fixed_Photo_Detector().translated(400, 300)

        wg = fp.LinkBetween(
            start=ec["op_0"],
            end=pd["op_0"],
            link_type=TECH.WG.SWG.C.WIRE,
            #
            # begin with port "op_0" of pdk.BendCircular
            start_factory=fp.ConstantFactory(result=(pdk.BendCircular(radius=40, degrees=45, waveguide_type=TECH.WG.FWG.C.WIRE), ("op_0", "op_1"))),
            #
            # end with port "op_0" of pdk.FWG2MWGTransition as "op_0" is FWG and "op_1" is MWG
            end_factory=EndFactory(),
        )

        insts += ec
        insts += pd
        insts += wg

        return insts, elems, ports


class EndFactory(fp.IWaveguideAdapterFactory):
    def __call__(self, end_types: Tuple[fp.IWaveguideType, fp.IWaveguideType]) -> Tuple[fp.ICurvedCellRef, Tuple[str, str]]:
        TECH = get_technology()
        assert isinstance(end_types[1], TECH.WG.FWG.C), "Unexpected end waveguide type"
        return pdk.FWG2MWGTransition(), ("op_1", "op_0")


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================

    library += LinkBetweenEndFactory()
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
