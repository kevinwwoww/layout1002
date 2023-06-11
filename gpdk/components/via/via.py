from dataclasses import dataclass

from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class Via(fp.PCell):
    """
    Attributes:
        top_layer: defaults to `LAYER.MT_DRW`, top layer
        via_layer: defaults to `LAYER.VIA2_DRW`, via layer
        bottom_layer: defaults to `LAYER.M2_DRW`, bottom layer
        top_shape: defaults to `VIAS.TOP_SHAPE`, top shape
        via_shape: defaults to `VIAS.VIA_SHAPE`, via shape
        bottom_shape: defaults to `VIAS.BOTTOM_SHAPE`, bottom shape
        port_names: defaults to ["ep_0", "ep_1"]

    Examples:
    ```python
    via = Via()
    fp.plot(via)
    ```
    ![Via](images/via.png)
    """

    top_layer: fp.ILayer = fp.LayerParam()
    via_layer: fp.ILayer = fp.LayerParam()
    bottom_layer: fp.ILayer = fp.LayerParam()
    top_shape: fp.IShape = fp.Param(type=fp.IShape)
    via_shape: fp.IShape = fp.Param(type=fp.IShape)
    bottom_shape: fp.IShape = fp.Param(type=fp.IShape)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["ep_0", "ep_1"])

    def _default_top_layer(self):
        return get_technology().LAYER.MT_DRW

    def _default_top_shape(self):
        return get_technology().VIAS.TOP_SHAPE

    def _default_via_layer(self):
        return get_technology().LAYER.VIA2_DRW

    def _default_via_shape(self):
        return get_technology().VIAS.VIA_SHAPE

    def _default_bottom_layer(self):
        return get_technology().LAYER.M2_DRW

    def _default_bottom_shape(self):
        return get_technology().VIAS.BOTTOM_SHAPE

    def build(self):
        insts, elems, ports = super().build()

        elems += fp.el.Polygon(self.top_shape, layer=self.top_layer)
        # ports += fp.Pin(name=self.port_names[0], position=(0, 0), shape=self.top_shape, layer=self.top_layer)

        elems += fp.el.Polygon(self.via_shape, layer=self.via_layer)

        elems += fp.el.Polygon(self.bottom_shape, layer=self.bottom_layer)
        # ports += fp.Pin(name=self.port_names[1], position=(0, 0), shape=self.bottom_shape, layer=self.bottom_layer)

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += Via()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
