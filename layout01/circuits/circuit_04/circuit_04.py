from fnpcell import all as fp
from gpdk import all as pdk
from layout01.technology import get_technology


@fp.pcell_class()
class Circuit04(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        builder = pdk.CompScanBuilder(width=2000, spacing=255, waveguide_type=TECH.WG.SWG.C.WIRE, fiber_coupler_adapter=pdk.GratingCoupler())
        builder.add_alignment()
        builder.add_title("Circuit04", layer=TECH.LAYER.LABEL_DRW)
        for i in range(10):
            builder.add_block(pdk.RingFilter(ring_radius=10 + i * 5, waveguide_type=TECH.WG.FWG.C.WIRE))

        insts += builder.build()

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================

    library += Circuit04()

    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
#
