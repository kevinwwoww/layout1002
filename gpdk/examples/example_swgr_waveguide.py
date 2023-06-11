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
    # fmt: off
    # fixed template end

    # custom region start
    euler_bend = fp.g.EulerBend(
        radians=math.pi/2,
        radius_min=5,
    )
    R = euler_bend.radius_eff
    euler_bend = euler_bend.translated(-R, -R*2)
    path = (
        fp.g.Path.move(to=euler_bend.first_point)
        .appended(euler_bend)
        .appended(euler_bend.c_mirrored(), reverse=True, end_at=(R, R*2))
    )

    wg = TECH.WG.SWGR.C.WIRE(curve=path)

    library += wg
    # custom region end

    # fixed template start
    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
    # fixed template end
