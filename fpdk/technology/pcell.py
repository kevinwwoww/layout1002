import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from fnpcell import all as fp


@dataclass(eq=False)
class PCellBase(fp.PCell):
    
    name: str = fp.NameParam(prefix="", hash=False, compare=False)
    

    @fp.cache()
    def sim_model(self, env: fp.ISimEnv) -> Optional[fp.ISimModel]:
        pcell_class = type(self)
        pcell_folder = Path(inspect.getabsfile(pcell_class)).parent

        try:
            return fp.sim.ExternalFileModel(path=(pcell_folder / pcell_class.__name__).with_suffix(".dat"))
        except Exception as e:
            from warnings import warn

            warn(f"Construct external file model error: {e}")
            return None
        
    
