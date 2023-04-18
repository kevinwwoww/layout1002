from dataclasses import dataclass
from fnpcell import all as fp
from AMFpdk_3_5_Cband.technology import get_technology
from typing import Tuple


@dataclass(eq=False)
class Via(fp.PCell):
    top_layer: fp.ILayer = fp.LayerParam()
    via_layer: fp.ILayer = fp.LayerParam()
    bottom_layer: fp.ILayer = fp.LayerParam()
    top_shape: fp.IShape = fp.Param(type=fp.IShape)
    via_shape: fp.IShape = fp.Param(type=fp.IShape)
    bottom_shape: fp.IShape = fp.Param(type=fp.IShape)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["ep_0", "ep_1"])

    def _default_top_layer(self):
        return get_technology().LAYER.MT2

    def _default_via_layer(self):
        return get_technology().LAYER.VIA2

    def _default_bottom_layer(self):
        return get_technology().LAYER.MT1

    def _default_top_shape(self):
        return get_technology().VIAS.TOP_SHAPE

    def _default_via_shape(self):
        return get_technology().VIAS.VIA_SHAPE

    def _default_bottom_shape(self):
        return get_technology().VIAS.BOTTOM_SHAPE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()

        elems += fp.el.Polygon(self.top_shape, layer=self.top_layer)
        elems += fp.el.Polygon(self.via_shape, layer=self.via_layer)
        # elems += fp.el.Rect(width=10, height=10, layer=TECH.LAYER.RIB, center=(10, 10))
        elems += fp.el.Polygon(self.bottom_shape, layer=self.bottom_layer)
        # bb = fp.el.PolygonSet.with_layer(self=aa, layer=TECH.LAYER.SINWG1)
        # elems += bb


        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk_3_5_Cband.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += Via()
    # Via().translated()
    # Via().h_mirrored()
    # Via().v_mirrored()
    # Via().c_mirrored()
    # Via().rotated()





    fp.export_gds(library, file=gds_file)
    fp.plot(library)
