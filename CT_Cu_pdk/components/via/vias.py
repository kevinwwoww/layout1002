import math
from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from CT_Cu_pdk.components.via.via import Via
from CT_Cu_pdk.technology import get_technology


@dataclass(eq=False)
class Vias(fp.PCell):
    width: float = fp.NonNegFloatParam(default=4)
    height: float = fp.NonNegFloatParam(default=4)
    spacing: float = fp.PositiveFloatParam()
    top_layer: fp.ILayer = fp.LayerParam()
    via_layer: fp.ILayer = fp.LayerParam()
    bottom_layer: fp.ILayer = fp.LayerParam()
    via: Via = fp.DeviceParam(type=Via)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["ep_0", "ep_1"])

    def _default_spacing(self):
        return get_technology().VIAS.SPACING

    def _default_top_layer(self):
        return get_technology().LAYER.M2

    def _default_via_layer(self):
        return get_technology().LAYER.Via1

    def _default_bottom_layer(self):
        return get_technology().LAYER.M1

    def _default_via(self):
        return Via(
            top_layer=self.top_layer,
            via_layer=self.via_layer,
            bottom_layer=self.bottom_layer,
            port_names=(None, None),
        )

    def __post_pcell_init__(self):
        assert self.spacing >= get_technology().VIAS.SPACING, f"requires spacing >= TECH.VIAS.SPACING, got: {self.spacing} >= {get_technology().VIAS.SPACING}"

    def build(self):
        insts, elems, ports = fp.InstanceSet(), fp.ElementSet(), fp.PortSet()
        width = self.width
        height = self.height
        spacing = self.spacing
        via = self.via

        (x_min, y_min), (x_max, y_max) = fp.get_bounding_box(via)
        w = x_max - x_min
        h = y_max - y_min

        width = max(width, w)
        height = max(height, h)
        m = max(1, math.floor((width + spacing) / (w + spacing)))
        n = max(1, math.floor((height + spacing) / (h + spacing)))

        col_width = width / m
        row_height = height / n
        spacing_x = (col_width - w) / 2
        spacing_y = (row_height - h) / 2

        via_array = via.new_array(
            cols=m,
            col_width=col_width,
            rows=n,
            row_height=row_height,
            transform=fp.translate(-x_min - width / 2 + spacing_x, -y_min - height / 2 + spacing_y),
        )

        insts += via_array

        return insts, elems, ports


if __name__ == "__main__":
    from CT_Cu_pdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    library += Vias()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
