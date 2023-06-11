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
    from gpdk.geometry.sampler_periodic import SamplerPeriodic

    path = fp.g.Polyline([(0.0, 0.0), (30.0, 0.0), (30.0, 20.0), (15.0, 30.0)])

    def content_for_sample2(sample: fp.SampleInfo):
        x, y = sample.position
        orientation = sample.orientation
        distance = 2
        dx = distance * math.cos(orientation + math.pi / 2)
        dy = distance * math.sin(orientation + math.pi / 2)
        return fp.Composite(
            fp.el.Rect(width=2, height=2, center=(0, 0), layer=TECH.LAYER.M1_DRW).translated(x + dx, y + dy),
            fp.el.Rect(width=2, height=2, center=(0, 0), layer=TECH.LAYER.M1_DRW).translated(x - dx, y - dy),
        )

    def content_for_sample1(sample: fp.SampleInfo):
        x, y = sample.position
        return fp.el.Rect(width=2, height=2, center=(0, 0), layer=TECH.LAYER.M1_DRW).translated(x, y)

    sampler = SamplerPeriodic(period=3, reserved_ends=(5, 5))

    mlt = TECH.METAL.MT.W20.updated(line_width=10)
    library += mlt(curve=path).with_patches(content_for_sample2(sample) for sample in sampler(path))

    r1, r2 = path.bundle(size=2, spacing=2 + 2)
    library += mlt(curve=path).with_patches([content_for_sample1(sample) for sample in sampler(r1) + sampler(r2)]).translated(40, 0)
    # custom region end

    # fixed template start
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
    # fixed template end
