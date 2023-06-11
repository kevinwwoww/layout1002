from dataclasses import dataclass
import math
from pathlib import Path
from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk.util.json_cell import JsonCell


@dataclass(eq=False)
class FixedBendEuler90(fp.IWaveguideLike, JsonCell, locked=True):
    json_name: fp.StrPath = "fixed_bend_euler_90"
    gds_name: fp.StrPath = "fixed_bend_euler_90"

    @property
    def radius_eff(self) -> float:
        return 10

    @property
    def raw_curve(self):
        return fp.g.FakeCurve(self.cell["op_0"], self.cell["op_1"], curve_length=16.828579272040376)
    
    @fp.cache()
    def sim_model(self, env: fp.ISimEnv):

        file_path = Path("BendCircular90_radius=10").with_suffix(".dat")

        return fp.sim.ExternalFileModel(file_path)


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    fixed_bend = FixedBendEuler90()
    R = fixed_bend.radius_eff
    ms = 150
    s = 30
    e = -30
    points = [(0, s), (0, 2 * R + ms), (-2 * R - ms, 2 * R + ms), (-2 * R - ms, 0), (e, 0), (e, -80)]

    def bend_factory(central_angle: float):
        if abs(central_angle) != math.pi / 2:
            raise NotImplementedError()
        result = fixed_bend if central_angle > 0 else fixed_bend.v_mirrored()
        return result, R, ("op_0", "op_1")

    library += fp.LinkSmooth(
        points,
        link_type=TECH.WG.FWG.C.WIRE,
        bend_factory=bend_factory
    )

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
