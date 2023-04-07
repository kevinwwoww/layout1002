from pathlib import Path
from typing import Any, Callable, Dict, FrozenSet, List, Mapping, Optional, Sequence, Tuple

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt

REQUIRED_ALL_FILES = Path("components") / "all.py"
REQUIRED_FUNC_ALL_FILES = Path("components") / "func_all.py"
REQUIRED_FOLDERS = ["components", "technology", REQUIRED_ALL_FILES, REQUIRED_FUNC_ALL_FILES]
NO_NEED_CHECK_MODULES = ["JsonCell", "Hard_Mask_WGTransition"]
TECHOLOGY_TECH_ATTRS = [
    "GDSII",
    "METRICS",
    "PIN",
    "PORT",
    "LABEL",
    "PROCESS",
    "PURPOSE",
    "LAYER",
    "DEVICE",
    "BAND",
    "WG",
    "METAL",
    "VIAS",
    "DISPLAY",
    "AUTO_TRANSITION",
    "AUTO_VIAS",
    "LINKING_POLICY",
    "FITTING_FUNCTION",
    "LINK_BETWEEN",
]
TECH_LAYERS_REQUIRED_CLASSES = ["PROCESS", "PURPOSE", "LAYER"]
TECH_BANDS_ATTRS = ["O", "E", "S", "C", "L", "U"]
SDL_SUPPORT_PARAMETER_TYPES: List[Any] = [
    str,
    int,
    float,
    Dict,
    FrozenSet,
    Path,
    bool,
    Callable,
    Sequence[Any],
    Sequence[Tuple[float, float]],
    Optional[str],
    Optional[int],
    Optional[float],
    fp.StrPath,
    Optional[fp.StrPath],
    fp.IWaypoints,
    fp.IWaylines,
    fpt.Layer,
    fp.IPort,
    fp.ICellRef,
    fp.Affine2D,
    fp.Anchor,
    fp.ILayer,
    fp.IBendWaveguideFactory,
    fp.ILinkingPolicy,
    fp.IDevice,
]
ANNOTATION_TO_DEFAULT_PARAMETER_TYPES_MAP: Mapping[Any, Any] = {
    fp.NameParam: str,
    fp.FloatParam: float,
    fp.DegreeParam: float,
    fp.NonNegFloatParam: float,
    fp.PositiveFloatParam: float,
    fp.IntParam: int,
    fp.PositiveIntParam: int,
    fp.NonNegIntParam: int,
    fp.BooleanParam: bool,
    fp.LayerParam: fp.ILayer,
    fp.AnchorParam: fp.Anchor,
    fp.PositionParam: fp.Point2D,
    fp.PortOptionsParam: fp.IPortOptions,
    fp.TransformParam: fp.Affine2D,
    fp.PointsParam: Sequence[fp.Point2D],
}
