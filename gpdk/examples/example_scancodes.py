from fnpcell import all as fp
from gpdk.technology import get_technology

if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    # =============================================================
    # fmt: off

    chars = "9527"
    scancodes = [
        fp.el.QRCode(data=chars, layer=TECH.LAYER.M1_DRW, pixel_size=5),
        fp.el.QRCode(data=chars, layer=TECH.LAYER.M1_DRW, pixel_size=5, invert=True).translated(180, 0),
        fp.el.DataMatrixCode(data=chars, layer=TECH.LAYER.M1_DRW, pixel_size=5).translated(0, 180),
        fp.el.DataMatrixCode(data=chars, layer=TECH.LAYER.M1_DRW, pixel_size=5, invert=True).translated(180, 180),
    ]
    library += fp.Composite(*scancodes).with_ports().with_name("scancodes")

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
