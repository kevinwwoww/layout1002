from pathlib import Path
from fnpcell.pdk.technology import all as fpt


class FontType(fpt.IFont, metaclass=fpt.GDSFontMeta):
    name = "Std Vented"
    file = Path(__file__).parent / "gdsii" / "std_vented.gds"


FONT = FontType()
