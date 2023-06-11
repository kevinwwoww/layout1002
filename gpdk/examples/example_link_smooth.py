import math
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology

if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    # fixed_bend = pdk.BendEuler90(radius_min=140, slab_square=True, waveguide_type=TECH.WG.FWG.C.WIRE)
    fixed_bend = pdk.BendCircular90(radius=140)
    R = fixed_bend.radius
    ms = 150
    s = 30
    e = -30
    # points = [(0, s), (0, 2 * R + ms), (-2 * R - ms, 2 * R + ms), (-2 * R - ms, 0), (e, 0)]
    points = [(0, -30), (0, R), (R, R), (2 * R, R), (2 * R , 0)]

    def bend_factory(central_angle: float):
        # if abs(central_angle) != math.pi / 2:
        #     raise NotImplementedError()
        result = fixed_bend if central_angle > 0 else fixed_bend.v_mirrored()
        print(central_angle)
        return result, R, ("op_0", "op_1")

    library += fp.LinkSmooth(
        points,
        start_type=TECH.WG.FWG.C.WIRE,
        end_type=TECH.WG.FWG.C.WIRE,
        link_type=TECH.WG.FWG.C.WIRE,
        bend_factory=bend_factory
    )

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
