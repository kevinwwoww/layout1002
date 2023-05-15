from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Tuple, List

from openpyxl import Workbook

from fnpcell.ansi.term import style, Color
from ..rule import CheckRule
from ..settings import REQUIRED_FOLDERS


@dataclass
class FileExistCheckRule(CheckRule):
    def checked(self, pdk: ModuleType, workbook: Workbook, index: int) -> Tuple[str, str]:
        contents: List[str] = []
        lack_folders: List[str] = []
        lack_files: List[str] = []
        title = "Checking [required folders and files]"
        worksheet = workbook.active  # type: ignore
        worksheet.cell(index, 1, f"required folders and files").font = self._font  # type: ignore
        self.title = title
        for folder in REQUIRED_FOLDERS:
            folder_path = Path(pdk.__path__[0]) / folder
            if folder_path.suffix != ".py" and (not folder_path.is_dir() or not folder_path.exists()):
                lack_folders.append(str(folder_path))
            elif folder_path.suffix == ".py" and (not folder_path.is_file() or not folder_path.exists()):
                lack_files.append(str(folder_path))

        if lack_folders or lack_files:
            lack_folders_ = "\n  ".join(lack_folders)
            lack_files_ = "\n  ".join(lack_files)
            contents += f"Missing required folders:\n  {lack_folders_}\n\n" if lack_folders else ""
            contents += f"Missing required files:\n  {lack_files_}\n" if lack_files else ""
            sty = style(color=Color.RED)
            self.style = sty
            contents_ = "".join(contents)
            return sty, f"[required folders and files]\n{contents_}\n"

        return "", ""
