from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk.technology.font.font_bombardier import FONT as font_bombardier
from gpdk.technology.font.font_college_tm import FONT as font_college_tm
from gpdk.technology.font.font_fff_forward import FONT as font_fff_forward
from gpdk.technology.font.font_fragile_bombers import FONT as font_fragile_bombers
from gpdk.technology.font.font_graduate import FONT as font_graduate
from gpdk.technology.font.font_karisma import FONT as font_karisma
from gpdk.technology.font.font_karnivore import FONT as font_karnivore

# from gpdk.technology.font.font_keania_one import FONT as font_keania_one
from gpdk.technology.font.font_line_pixel_7 import FONT as font_line_pixel_7
from gpdk.technology.font.font_minercraftory import FONT as font_minercraftory
from gpdk.technology.font.font_pop_warner import FONT as font_pop_warner
from gpdk.technology.font.font_press_start_2p import FONT as font_press_start_2p
from gpdk.technology.font.font_staubach import FONT as font_staubach

# from gpdk.technology.font.font_zcool_qingke_huangyou import FONT as font_zcool_qingke_huangyou
from gpdk.technology.font.font_std_vented import FONT as font_std_vented
from gpdk.technology.font.font_traceroute import FONT as font_traceroute
from gpdk.technology.font.font_your_complex_brk import FONT as font_your_complex_brk

if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    # =============================================================

    chars = " #+-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_"  # abcdefghijklmnopqrstuvwxyz"
    fonts = [
        font_bombardier,
        font_college_tm,
        font_fff_forward,
        font_fragile_bombers,
        font_graduate,
        font_karisma,
        font_karnivore,
        # font_keania_one,
        font_line_pixel_7,
        font_minercraftory,
        font_pop_warner,
        font_press_start_2p,
        font_staubach,
        font_traceroute,
        font_your_complex_brk,
        # font_zcool_qingke_huangyou,
        font_std_vented,
    ]
    labels = [
        fp.el.Label(content=font.name.upper() + chars, at=(0, i * 40), layer=TECH.LAYER.TEXT_NOTE, font=font, font_size=15) for i, font in enumerate(fonts)
    ]
    labels += [
        fp.el.Label(content=font.name.upper() + chars, at=(2000, i * 40), layer=TECH.LAYER.TEXT_NOTE, font=font, font_size=15, highlight=True)
        for i, font in enumerate(fonts)
    ]
    library += fp.Composite(*labels).with_ports().with_name("fonts")

    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
