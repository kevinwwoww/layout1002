import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import FrozenSet, Iterable, Optional, Tuple

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt


@dataclass(eq=False)
class GdsCell(fp.PCell):
    gds_folder: fp.StrPath = fp.Param()
    gds_name: fp.StrPath = fp.Param()
    gds_path: fp.StrPath = fp.Param()
    cell_name: Optional[str] = fp.TextParam(required=False)
    ignore_layers: FrozenSet[Tuple[int, int]] = fp.SetParam(immutable=True)

    def _default_gds_folder(self) -> str:
        return str(Path(inspect.getfile(type(self))).parent)

    def _default_gds_name(self) -> str:
        return type(self).__name__

    def _default_gds_path(self) -> str:
        return str((Path(self.gds_folder) / self.gds_name).with_suffix(".gds"))

    def _default_ignore_layers(self) -> FrozenSet[Tuple[int, int]]:
        return frozenset()

    def layer_mapper(self, value: Tuple[int, int]) -> Optional[fpt.ILayer]:
        if value in self.ignore_layers:
            return None
        return fpt.get_technology().LAYER(value)

    def cell_ports(self) -> Optional[Iterable[fpt.ITerminal]]:
        return None

    def build(self):
        insts, elems, ports = super().build()
        cell = fp.import_from_gds(file=self.gds_path, cell_name=self.cell_name, layer_mapper=self.layer_mapper, ports=self.cell_ports()).cell
        for it in cell.content:
            if isinstance(it, fpt.ICellRef):  # instance
                insts += it
            else:  # element
                elems += it
        ports += cell.ports
        return insts, elems, ports
