import random
from typing import Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk.technology.font.font_pop_warner import FONT as font_pop_warner


class Welcome(fp.PCell):
    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        instSet, elemSet, portSet = super().build()
        TECH = get_technology()

        period_x = 1
        period_y = 1
        rows = 5
        cols = 20

        layer1 = TECH.LAYER.FWG_CLD
        layer2 = TECH.LAYER.SWG_CLD
        layer3 = TECH.LAYER.MWG_CLD
        layers = [layer1, layer2, layer3]

        for i in range(rows):
            for j in range(cols):
                uc = fp.el.Rect(width=1, height=1, center=(0, 0), layer=random.choice(layers)).translated(j * period_x, i * period_y)
                elemSet += uc

        label = fp.el.Label(
            content="Welcome to PhotoCAD", font_size=2, font=font_pop_warner, at=(9.5, -2.5), anchor=fp.Anchor.CENTER, layer=TECH.LAYER.FLYLINE_MARK
        )
        elemSet += label

        for i in range(rows):
            for j in range(cols):
                uc = fp.el.Rect(width=1, height=1, center=(0, 0), layer=random.choice(layers)).translated(j * period_x, i * period_y - 7)
                elemSet += uc

        return instSet, elemSet, portSet


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    library += Welcome()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
