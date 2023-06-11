from fnpcell import all as fp
from gpdk.technology import get_technology


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    # =============================================================

    pn_paint = fp.el.CurvePaint.from_profile(
        [
            (TECH.LAYER.P_DRW, [(0, [12])], (0, 0)),
            (TECH.LAYER.N_DRW, [(3, [8])], (0, 0)),
        ]
    )
    library += fp.Composite(pn_paint(fp.g.Line(20), offset=-10, final_offset=20, extension=(5, 5))).with_ports().with_name("pn_paint_s")

    curve = fp.g.Polyline(raw_points=[(0, 0), (200, 0), (250, 50)])

    library += (
        fp.Composite(pn_paint(curve, offset=-10, final_offset=20, extension=(15, 15)), fp.el.Curve(curve, layer=TECH.LAYER.PAYLOAD_NOTE))
        .with_ports()
        .with_name("pn_paint")
    )

    slot_paint = fp.el.CurvePaint.ContinuousLayer(layer=TECH.LAYER.DT_DRW, width=36, final_width=80, offset=20, final_offset=-40).with_slots(
        max_width=35, slot_width=3
    )
    library += (
        fp.Composite(slot_paint(curve, offset=-10, final_offset=20, extension=(15, 15)), fp.el.Curve(curve, layer=TECH.LAYER.PAYLOAD_NOTE))
        .with_ports()
        .with_name("slot_paint")
    )

    crack_paint = fp.el.CurvePaint.ContinuousLayer(layer=TECH.LAYER.DT_DRW, width=36, final_width=80, offset=20, final_offset=-40).with_cracks(
        max_width=35, spacing=3
    )
    library += (
        fp.Composite(crack_paint(curve, offset=-10, final_offset=20, extension=(15, 15)), fp.el.Curve(curve, layer=TECH.LAYER.PAYLOAD_NOTE))
        .with_ports()
        .with_name("crack_paint")
    )

    wg = TECH.WG.FWG.C.WIRE(curve=fp.g.Line(30), offset=-10, final_offset=20)
    library += wg

    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
