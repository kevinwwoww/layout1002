from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.examples.mesh_mzi import MZI
from gpdk.technology import WG, get_technology
from gpdk.routing.extended.extended import Extended
from gpdk.technology.waveguide_factory import EulerBendFactory
from gpdk.components.grating_coupler.grating_coupler import GratingCoupler
from gpdk.routing.comp_scan.comp_scan import CompScan,Block


@dataclass(eq=False)
class MZI_triangle_mesh_with_GC(fp.PCell, band="C"):
    """
    Attributes:
        p_width: defaults to 1
        n_width: defaults to 1
        np_offset: defaults to 0
        wg_length: defaults to 25
        arm_spacing: defaults to 100
        dc_length: defaults to 100
        waveguide_type: type of waveguide
        pn_phase_shifter: instance of `PnPhaseShifter`, port_count=2, pin_count=2, required=False
        straight_waveguide: instance of `Straight`, port_count=2, required=False
        directional_coupler_left: instance of `DirectionalCouplerSBend`, port_count=2, required=False
        directional_coupler_right: instance of `DirectionalCouplerSBend`, port_count=2, required=False
        port_names: defaults to ["op_0", "op_1", "op_2", "op_3"]

    Examples:
    ```python
    TECH = get_technology()
    mzi = MZI(wg_length=600, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(mzi)
    ```
    ![MZI](images/mzi.png)
    """

    side_length: float = fp.PositiveFloatParam(default=400)
    dc_length: float = fp.FloatParam(default=100)
    arm_spacing: float = fp.FloatParam(default=60)
    wg_length: float = fp.FloatParam(default=100)
    gc_spacing: float = fp.FloatParam(default=50)
    waveguide_type: WG.FWG.C = fp.WaveguideTypeParam(type=WG.FWG.C)
    MZI_unit: fp.IDevice = fp.DeviceParam(type=MZI, port_count=4, required=False)
    grating_coupler: fp.IDevice = fp.DeviceParam(type=GratingCoupler, port_count=1, required=False)

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def _default_MZI_unit(self):
        return MZI(waveguide_type=self.waveguide_type, arm_spacing=self.arm_spacing,
                   dc_length=self.dc_length, wg_length=self.wg_length)

    def _default_grating_coupler(self):
        return GratingCoupler(waveguide_type=self.waveguide_type)

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        # fmt: off

        waveguide_type = self.waveguide_type
        port_names = self.port_names
        MZI_0 = self.MZI_unit.translated(0,0)
        MZI_1 = self.MZI_unit.rotated(degrees=120).translated(self.side_length / 4, self.side_length / 4 * (3) ** (0.5))
        MZI_2 = self.MZI_unit.rotated(degrees=60).translated(-self.side_length / 4, self.side_length / 4 * (3) ** (0.5))
        MZI_3 = self.MZI_unit.translated(self.side_length / 2, self.side_length / 2 * (3) ** (0.5))
        MZI_4 = self.MZI_unit.rotated(degrees=60).translated(self.side_length * 3 / 4, self.side_length / 4 * (3) ** (0.5))
        gc_0 = self.grating_coupler.rotated(degrees=180).translated(-self.side_length / 4 * 3, -self.gc_spacing)
        gc_1 = self.grating_coupler.rotated(degrees=180).translated(-self.side_length / 4 * 3, 10)
        gc_2 = self.grating_coupler.rotated(degrees=180).translated(-self.side_length / 4 * 3, self.side_length / 2 * (3) ** (0.5) - 10 )
        gc_3 = self.grating_coupler.rotated(degrees=180).translated(-self.side_length / 4 * 3, self.side_length / 2 * (3) ** (0.5) + self.gc_spacing)
        gc_4 = self.grating_coupler.translated(-self.side_length / 4 * 3 + self.side_length * 2, -self.gc_spacing)
        gc_5 = self.grating_coupler.translated(-self.side_length / 4 * 3 + self.side_length * 2, 10)
        gc_6 = self.grating_coupler.translated(-self.side_length / 4 * 3 + self.side_length * 2,
                                                                    self.side_length / 2 * (3) ** (0.5) - 10)
        gc_7 = self.grating_coupler.translated(-self.side_length / 4 * 3 + self.side_length * 2,
                                                                    self.side_length / 2 * (3) ** (0.5) + self.gc_spacing)
        insts += fp.Linked(
            link_type=waveguide_type,
            bend_factory=self.waveguide_type.BEND_EULER,
            links=[
                MZI_0["op_1"] >> gc_0["op_0"],
                MZI_2["op_0"] >> gc_1["op_0"],
                MZI_2["op_3"] >> gc_2["op_0"],
                MZI_3["op_0"] >> gc_3["op_0"],
                MZI_0["op_2"] >> gc_4["op_0"],
                MZI_4["op_1"] >> gc_5["op_0"],
                MZI_4["op_2"] >> gc_6["op_0"],
                MZI_3["op_3"] >> gc_7["op_0"],
                MZI_0["op_0"] >> MZI_2["op_1"],
                MZI_0["op_3"] >> MZI_1["op_0"],
                MZI_1["op_1"] >> MZI_4["op_0"],
                MZI_4["op_3"] >> MZI_3["op_2"],
                MZI_1["op_2"] >> MZI_3["op_1"],
                MZI_1["op_3"] >> MZI_2["op_2"],
            ],
            ports=[],
        )
        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    mesh = MZI_triangle_mesh_with_GC()
    library += mesh

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
