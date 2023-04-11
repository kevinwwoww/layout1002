from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional

from fnpcell import all as fp


@dataclass(eq=False)
class JsonCell(fp.PCell):
    root_folder: fp.StrPath = fp.Param()
    stem_name: fp.StrPath = fp.Param()
    json_folder: fp.StrPath = fp.Param()
    json_name: fp.StrPath = fp.Param()
    json_path: fp.StrPath = fp.Param()
    gds_folder: Optional[fp.StrPath] = fp.Param(required=False)
    gds_name: Optional[fp.StrPath] = fp.Param(required=False)
    gds_path: Optional[fp.StrPath] = fp.Param(required=False)
    default_layers: Mapping[str, Any] = fp.MappingParam(immutable=True)
    sparam_folder: Optional[fp.StrPath] = fp.Param(required=False)
    sparam_name: Optional[fp.StrPath] = fp.Param(required=False)
    sparam_path: Optional[fp.StrPath] = fp.Param(required=False)

    def _default_name(self) -> str:
        return str(self.stem_name) if type(self) == JsonCell else ""

    def _default_root_folder(self) -> fp.StrPath:
        return "."

    def _default_stem_name(self) -> fp.StrPath:
        return type(self).__name__

    def _default_json_folder(self) -> fp.StrPath:
        return self.root_folder

    def _default_json_name(self) -> fp.StrPath:
        return self.stem_name

    def _default_json_path(self) -> fp.StrPath:
        return (Path(self.json_folder) / self.json_name).with_suffix(".json")

    def _default_gds_folder(self) -> fp.StrPath:
        return self.root_folder

    def _default_gds_name(self) -> fp.StrPath:
        return self.gds_name

    def _default_gds_path(self) -> Optional[fp.StrPath]:
        gds_folder = self.gds_folder
        gds_name = self.gds_name
        if gds_folder is None or gds_name is None:
            return None
        gds_path = (Path(gds_folder) / gds_name).with_suffix(".gds")
        return gds_path

    def _default_default_layers(self) -> Mapping[str, Any]:
        return fp.FrozenDict({"*": "_AUTO_"})

    def _default_sparam_folder(self) -> fp.StrPath:
        return self.root_folder

    def _default_sparam_name(self) -> fp.StrPath:
        return self.stem_name

    def _default_sparam_path(self) -> Optional[fp.StrPath]:
        sparam_folder = self.sparam_folder
        sparam_name = self.sparam_name
        if sparam_folder is None or sparam_name is None:
            return None
        sparam_path = (Path(sparam_folder) / sparam_name).with_suffix(".dat")
        return sparam_path

    def build(self):
        insts, elems, ports = super().build()
        cell = fp.import_from_json(name=self.name, json_path=self.json_path, library_path=self.gds_path, default_layers=self.default_layers).cell
        for it in cell.content:
            if isinstance(it, fp.ICellRef):  # instance
                insts += it
            else:  # element
                elems += it
        ports += cell.ports
        return insts, elems, ports

    @fp.cache()
    def sim_model(self, env: fp.ISimEnv) -> Optional[fp.ISimModel]:
        sparam_path = self.sparam_path
        if sparam_path is None:
            return None
        try:
            return fp.sim.ExternalFileModel(path=sparam_path)
        except Exception as e:
            from warnings import warn

            warn(f"Construct external file model error: {e}")
            return None
