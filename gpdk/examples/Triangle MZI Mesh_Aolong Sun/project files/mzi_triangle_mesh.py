from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.examples.mesh_mzi import MZI
from gpdk.technology import WG, get_technology
from gpdk.routing.extended.extended import Extended
from gpdk.technology.waveguide_factory import EulerBendFactory, CircularBendFactory
from gpdk.components.grating_coupler.grating_coupler import GratingCoupler
from gpdk.routing.comp_scan.comp_scan import CompScan,Block


@dataclass(eq=False)
class MZI_triangle_mesh(fp.PCell, band="C"):
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
    waveguide_type: WG.FWG.C = fp.WaveguideTypeParam(type=WG.FWG.C)
    MZI_unit: fp.IDevice = fp.DeviceParam(type=MZI, port_count=4, required=False)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=8,
                default=["op_0", "op_1", "op_2", "op_3", "op_4", "op_5", "op_6", "op_7"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def _default_MZI_unit(self):
        return MZI(waveguide_type=self.waveguide_type, arm_spacing=self.arm_spacing,
                   dc_length=self.dc_length, wg_length=self.wg_length)

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
        # MZI_6 = self.MZI_unit.translated(self.side_length *2  / 2, 0)
        ports += MZI_3["op_0"].with_name(port_names[0])
        ports += MZI_2["op_3"].with_name(port_names[1])
        ports += MZI_2["op_0"].with_name(port_names[2])
        ports += MZI_0["op_1"].with_name(port_names[3])
        ports += MZI_0["op_2"].with_name(port_names[4])
        ports += MZI_4["op_1"].with_name(port_names[5])
        ports += MZI_4["op_2"].with_name(port_names[6])
        ports += MZI_3["op_3"].with_name(port_names[7])

        # insts += MZI_6

        insts += fp.Linked(
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER,
            links=[
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
    def bend_factories(waveguide_type: fp.IWaveguideType):
        return TECH.WG.FWG.C.WIRE.BEND_EULER

    def gc_factory(at: fp.IRay, device: fp.IDevice):
        return GratingCoupler(), "op_0"

    mesh = MZI_triangle_mesh()
    library += mesh
    #
    # blocks = [Block(mesh)]
    # library += CompScan(
    #     name="comp_scan",
    #     spacing=200,
    #     width=1000,
    #     blocks=blocks,
    #     bend_factories=bend_factories,
    #     waveguide_type=TECH.WG.FWG.C.WIRE,
    #     connection_type=TECH.WG.FWG.C.WIRE,
    #     fiber_coupler_factory=gc_factory,
    # )



    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
