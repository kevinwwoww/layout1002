from typing import Any, Callable, Dict, Iterable, List, Optional, Union

from fnpcell import all as fp
from AMFpdk.technology import get_technology


def combine_builds(name: str, specs: Iterable[Dict[str, Any]]) -> fp.IDevice:
    result: List[fp.IElement] = []
    for spec in specs:
        source: Union[None, fp.ICell, fp.ICellRef, Callable[[], fp.ICellRef]] = spec.get("source")

        if source is not None:
            if isinstance(source, Callable):
                future = source()  # type: ignore
            elif isinstance(source, fp.ICellRef):
                future = source
            else:
                assert isinstance(source, fp.ICell), f"Unsupported source type [{type(source)}], label: [{spec['label']}]"
                future = source.new_ref()
            spec["source"] = future

    for spec in specs:
        instance: Optional[fp.ICellRef] = spec.get("source")
        origin = spec["origin"]

        ox, oy = origin
        if instance is not None:
            (x_min, y_min), (x_max, y_max) = fp.get_bounding_box(instance)
            width, height = x_max - x_min, y_max - y_min
            origin = ox - x_min, oy - y_min  # (x_min + x_max) / 2, (y_min + y_max) / 2
            instance = instance.translated(*origin)
            result.append(instance)
        else:
            width, height = spec["dimensions"]

        tx = ox + width / 2
        ty = oy + height / 2
        LAYER = get_technology().LAYER
        rect = fp.el.Rect(width=width, height=height, center=(tx, ty), layer=LAYER.LBL)
        label = fp.el.Label(spec["label"], baseline=fp.TextBaseline.BOTTOM, layer=LAYER.LBL)

        w, h = label.size
        sx, sy = width / w, height / h
        s = sx if sx < sy else sy

        label = label.scaled(s).translated(tx - s * w / 2, ty - s * h / 2)

        result.append(rect)
        result.append(label)

    return fp.Device(name=name, content=result, ports=[])
#