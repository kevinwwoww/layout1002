import inspect
import re
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Iterable, List, Set, Tuple, TypeVar, Union, cast

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt
from IMECAS_SiN_pdk.technology import get_technology

_T = TypeVar("_T", bound=Callable[..., Union[fp.ICell, fp.ICellRef, fp.ILibrary]])


def expect_same_content(
    gds_folder: fp.StrPath = "snapshot",
    gds_filename: Union[Tuple[str, str], fp.StrPath] = (r"test_(\w+)", r"\1"),
    ignore_layers: Iterable[fp.ILayer] = (),
    plot_differences: bool = False,
    snap_to_grid: bool = False,
):
    ignore_layers = frozenset(ignore_layers)

    def compare_content(test_fn: _T) -> _T:
        @wraps(test_fn)
        def test_wrapper(*args: Any, **kwargs: Any) -> Any:
            result = test_fn(*args, **kwargs)

            cwd = Path(inspect.getfile(test_fn)).parent
            filename = gds_filename
            if isinstance(filename, Tuple):
                filename = re.sub(filename[0], filename[1], test_fn.__name__)
            gds_file = (cwd / gds_folder / filename).with_suffix(".gds")

            if not gds_file.exists():
                fp.export_gds(result, file=gds_file)
                return

            user_unit = fpt.user_unit()
            with fp.BinaryResource(gds_file) as input:
                importer = fp.util.GDSImporter(input, user_unit=user_unit)

            snapshot_layer_mapper = _CollectingLayerMapper()
            snapshot_cells = importer.top_cells(snapshot_layer_mapper)

            file = fp.util.BytesIO()
            fp.export_gds(result, file=file)
            result_layer_mapper = _CollectingLayerMapper()
            with file:
                result_cells = fp.util.GDSImporter(file, user_unit=user_unit).top_cells(result_layer_mapper)

            layers_diff = result_layer_mapper.layers - snapshot_layer_mapper.layers
            assert not layers_diff, f"Layers not found in snapshot: {[it.name for it in layers_diff]}"

            layers_diff = snapshot_layer_mapper.layers - result_layer_mapper.layers
            assert not layers_diff, f"Layers not found in result: {[it.name for it in layers_diff]}"

            differences: List[fp.IPolygonSet] = []
            for layer in result_layer_mapper.layers:
                if layer in ignore_layers:
                    continue
                result_polygon_sets = [cell.polygon_set(layer=layer) for cell in result_cells]
                snapshot_polygon_sets = [cell.polygon_set(layer=layer) for cell in snapshot_cells]
                if len(result_polygon_sets) == 0 and len(snapshot_polygon_sets) == 0:
                    continue
                if len(snapshot_polygon_sets) == 0:
                    raise AssertionError(f"Polygons for [{layer.name}] not found in snapshot")
                if len(result_polygon_sets) == 0:
                    raise AssertionError(f"Polygons for [{layer.name}] not found in result")

                snapshot_polygon_set = fp.el.PolygonSet.boolean_or(*snapshot_polygon_sets, layer=layer)
                result_polygon_set = fp.el.PolygonSet.boolean_or(*result_polygon_sets, layer=layer)

                if snap_to_grid:
                    snapshot_polygon_set = _snap_to_grid(snapshot_polygon_set)
                    result_polygon_set = _snap_to_grid(result_polygon_set)

                xor = snapshot_polygon_set ^ result_polygon_set
                if xor.polygons:
                    if plot_differences:
                        differences.append(xor)
                    else:
                        raise AssertionError(f"PolygonSets for [{layer.name}] are not equal")

            if differences:
                fp.plot(fp.Composite(differences), title=f"{test_fn.__name__}")
                raise AssertionError(f"PolygonSets for {[it.layer.name for it in differences]} are not equal")

            return None  # result

        return cast(_T, test_wrapper)

    return compare_content


class _CollectingLayerMapper:
    layers: Set[fp.ILayer]

    def __init__(self):
        self.layers = set()

    def __call__(self, value: Tuple[int, int]):
        TECH = get_technology()
        try:
            layer = TECH.LAYER(value)
        except:
            layer = fp.UnknownLayer(value)
        self.layers.add(layer)
        return layer


def _snap_to_grid(polygon_set: fp.IPolygonSet) -> fp.IPolygonSet:
    layer = polygon_set.layer
    polygons: List[fp.IPolygon] = []
    for polygon in polygon_set:
        points = [fp.snap_to_grid(point) for point in polygon.polygon_points]
        polygons.append(fp.el.Polygon(points, layer=layer))
    return fp.el.PolygonSet(polygons, layer=layer)
