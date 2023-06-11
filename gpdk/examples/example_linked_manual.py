from dataclasses import dataclass
from typing import Optional, Sequence, Tuple
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(frozen=True)
class EulerBendFactory:
    radius_min: float
    l_max: Optional[float] = None

    def __call__(self, central_angle: float):
        bend = fp.g.EulerBend(radians=central_angle, radius_min=self.radius_min, l_max=self.l_max)
        return bend, bend.radius_eff


@dataclass(eq=False)
class LinkedGratingCoupler(fp.PCell):
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(default=get_technology().WG.SWG.C.WIRE, doc="Waveguide parameters")
    gc_pcell: fp.IDevice = fp.DeviceParam(type=pdk.GratingCoupler, port_count=1)
    points: Sequence[fp.Point2D] = fp.PointsParam(min_count=2, doc="control points, count >= 2, eg. [(x1, y1), (x2, y2)]")

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        # =============================================================
        # =============== instance list, rotate and mirror =======================
        gc = self.gc_pcell.h_mirrored(x=0)
        gc2 = self.gc_pcell
        link = self.waveguide_type(curve=fp.g.Path.smooth(self.points, bend_factory=EulerBendFactory(radius_min=5)))
        # ====================== instance place =======================
        gc1 = gc.translated(-10, 0)
        # =============== connection with port_pair ====================
        device = fp.Connected(
            joints=[
                gc1["op_0"] <= link["op_0"],
                link["op_1"] <= gc2["op_0"],
            ],
            ports=[],
        )
        insts += device
        # =============================================================
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    wg_type = TECH.WG.FWG.C.WIRE
    gc = pdk.GratingCoupler(waveguide_type=wg_type)
    library += LinkedGratingCoupler(gc_pcell=gc, points=[(0, 0), (100, 0), (100, 100), (200, 100)], waveguide_type=wg_type)

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
