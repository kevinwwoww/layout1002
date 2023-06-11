import math
from fnpcell import all as fp
from gpdk.technology import get_technology


if __name__ == "__main__":
    # fixed template start
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    # =============================================================
    # fixed template end

    # custom region start
    path = fp.g.Polyline([(0.0, 0.0), (30.0, 0.0), (30.0, 20.0), (15.0, 30.0)])
    extension_profile = [
        (
            TECH.LAYER.M1_DRW,
            [
                (2, [3]),
                (-2, [3]),
            ],
            (5, 10),
        )
    ]

    mlt = TECH.METAL.MT.W20.updated(line_width=10)
    library += (
        mlt(curve=path)
        .with_patches(
            [
                fp.el.Curve(path.extended(extension), stroke_width=widths[0], stroke_offset=offset, layer=layer, miter_limit=math.inf)
                for layer, spec, extension in extension_profile
                for offset, widths in spec
            ]
        )
        .with_name("extension_profile")
    )

    # custom region end

    # fixed template start
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
    # fixed template end
