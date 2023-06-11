from dataclasses import dataclass
from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class PolygonBooleanOps(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off

        rect = fp.el.Rect(width=40, height=30, center=(0, 0), layer=TECH.LAYER.MT_DRW)
        for i in range(3):
            elems += rect.translated(i * 40, 0).rotated(degrees=30)

        d_1 = fp.Device(content=[insts, elems], ports=ports)

        d_2 = d_1.translated(0, -20).content_merged(affected_layer=[TECH.LAYER.MT_DRW])
        insts += d_2

        vc_arc2 = fp.el.EllipticalArc(radius=10, origin=(0, 10), stroke_width=5, layer=TECH.LAYER.CONT_DRW)
        vc_rect = fp.el.Rect(width=30, height=2, center=(0, 18), layer=TECH.LAYER.CONT_DRW)
        elems += vc_arc2
        elems += vc_rect
        vc_1 = vc_arc2 - vc_rect
        elems += fp.el.Group(vc_1).translated(30, 0)
        vc_2 = vc_arc2 | vc_rect
        elems += fp.el.Group(vc_2).translated(60, 0)
        vc_3 = vc_arc2 & vc_rect
        elems += fp.el.Group(vc_3).translated(90, 0)
        vc_4 = vc_rect ^ vc_arc2
        elems += fp.el.Group(vc_4).translated(120, 0)

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    device = PolygonBooleanOps()
    library += device
    mt = device.polygon_set(layer=TECH.LAYER.MT_DRW)
    cont = device.polygon_set(layer=TECH.LAYER.CONT_DRW)
    m2 = fp.el.PolygonSet.boolean_sub(mt, cont, layer=TECH.LAYER.M2_DRW)
    device2 = fp.Device(content=m2, ports=[]).with_name("layer_boolean_sub")
    library += device2.translated(0, 150)
    (x_min, y_min), (x_max, y_max) = fp.get_bounding_box(device, exclude_layers=[TECH.LAYER.PINREC_NOTE, TECH.LAYER.PINREC_TEXT])
    cont_invert = device.polygon_set(layer=TECH.LAYER.CONT_DRW).inverted(fp.g.Shape([(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]))
    device3 = fp.Device(content=cont_invert, ports=[]).with_name("layer_boolean_invert")
    library += device3.translated(0, 300)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
