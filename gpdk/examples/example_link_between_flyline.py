import warnings
from dataclasses import dataclass

from fnpcell import all as fp
from fnpcell.errors import FlylineWarning
from fnpcell.pdk.technology import all as fpt
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(frozen=True)
class CircularBendFactory(fpt.IBendWaveguideFactory):
    radius_eff: float

    def __call__(self, central_angle: float):
        import math
        from gpdk.components.bend.bend_circular import BendCircular90_FWG_C_WIRE

        radius_eff = self.radius_eff

        bend = None
        if fp.is_close(abs(central_angle), math.pi / 2):
            bend = BendCircular90_FWG_C_WIRE()

            if bend and central_angle < 0:
                bend = bend.v_mirrored()

        if bend is None:
            raise NotImplementedError("Only 90 degrees bends are supported")

        return bend, radius_eff, ("op_0", "op_1")


if __name__ == "__main__":
    from gpdk.components import all as components
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================

    # port0 and port1 are too close for bend
    ec = pdk.Fixed_Edge_Coupler().translated(0, -3)
    pd = pdk.Fixed_Photo_Detector().translated(400, 0)

    # so there will be flyline between them
    warnings.simplefilter(action="ignore", category=FlylineWarning)  # raises if there's FlylineWarning
    wg = fp.LinkBetween(
        start=ec["op_0"], end=pd["op_0"], link_type=TECH.WG.FWG.C.WIRE, bend_factory=CircularBendFactory(radius_eff=10), flyline_layer=TECH.LAYER.FLYLINE_MARK
    )
    library += fp.Device(content=[ec, pd, wg], ports=[]).with_name("flyline")
    fp.export_gds(library, file=gds_file)
    fp.export_spc(library, file=gds_file.with_suffix(".spc"), components=components)
    fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=components)
    # fp.plot(library)

    # if we want an error of FlylineWarning
    warnings.simplefilter(action="error", category=FlylineWarning)  # raises if there's FlylineWarning
    try:
        wg = fp.LinkBetween(start=ec["op_0"], end=pd["op_0"], link_type=TECH.WG.FWG.C.WIRE, bend_factory=CircularBendFactory(radius_eff=10))
        fp.plot(wg)  # type: ignore # Never called
        raise AssertionError("Unreachable assertion")
    except FlylineWarning as e:
        pass
    # =============================================================
    # fp.export_gds(library, file=gds_file)
    # fp.plot(library)
