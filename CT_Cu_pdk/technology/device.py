from typing import Iterable
from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt


class DEVICE:
    @fpt.classconst
    @classmethod
    def BAND_LAYER(cls):
        from CT_Cu_pdk.technology import get_technology
        return get_technology().LAYER.TEXT_NOTE

    @classmethod
    def band_annotation(cls, cell: fpt.ICell, bands: Iterable[fpt.IBand]):
        from CT_Cu_pdk.technology import get_technology

        label = ",".join(band.name for band in bands)
        if not label:
            return None

        (x_min, y_min), (x_max, y_max) = fp.get_bounding_box(cell)

        width, height = x_max - x_min, y_max - y_min
        if not width or not height:
            return None

        origin = (x_min + x_max) / 2, (y_min + y_max) / 2

        DEVICE = get_technology().DEVICE
        rect = fp.el.Rect(
            width=width,
            height=height,
            center=origin,
            layer=DEVICE.BAND_LAYER,
        )

        # w, h = label.size
        # sx, sy = width / w, height / h
        # s = sx if sx < sy else sy
        # tx, ty = origin
        # label = label.scaled(s).translated(tx - s * w / 2, ty - s * h / 2)

        w = 5
        h = 5
        sx, sy = width / w, height / h
        s = sx if sx < sy else sy
        tx = x_min + 0.2
        ty = y_min + 0.2

        label = label.scaled(s).translated(tx, ty)

        return fp.el.Group(rect, label)
