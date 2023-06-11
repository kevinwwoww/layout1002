from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class CurveLength(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        # fmt: off
        TECH = get_technology()

        fwg_ring_filter = pdk.RingFilter(name="f0", ring_radius=100, waveguide_type=TECH.WG.FWG.C.WIRE)
        insts += fwg_ring_filter

        port_spacing = fp.distance_between(fwg_ring_filter["op_0"].position, fwg_ring_filter["op_1"].position)

        x = fwg_ring_filter["op_0"].position[0]-20
        y = (fwg_ring_filter["op_0"].position[1]+fwg_ring_filter["op_1"].position[1])/2
        distance = fp.el.Text(fr"{port_spacing}", text_anchor=fp.Anchor.CENTER, at=(x, y), layer=TECH.LAYER.MT_DRW)
        elems += distance

        bend = pdk.BendEuler(radius_min=50, degrees=-90, waveguide_type=TECH.WG.FWG.C.WIRE)
        insts += bend
        elems += fp.el.Text(f"{bend.curve_length}", at=bend.curve.last_point, layer=TECH.LAYER.MT_DRW)

        for i in range(1, 11):
            radius_min = i * 20
            euler_bend = fp.g.EulerBend(radius_min=radius_min, degrees=90, l_max=60)

            elems += fp.el.Curve(euler_bend, stroke_width=1, layer=TECH.LAYER.MT_DRW)
            elems += fp.el.Text(f"{euler_bend.curve_length}", at=euler_bend.last_point, layer=TECH.LAYER.MT_DRW)

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += CurveLength()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
