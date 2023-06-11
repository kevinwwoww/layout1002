from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from gpdk.components.directional_coupler.directional_coupler_sbend import DirectionalCouplerSBend
from gpdk.components.straight.straight import Straight
from gpdk.components.pn_phase_shifter.pn_phase_shifter import PnPhaseShifter
from gpdk.technology import WG, get_technology


@dataclass(eq=False)
class MZI(fp.PCell, band="C"):
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

    p_width: float = fp.PositiveFloatParam(default=1)
    n_width: float = fp.PositiveFloatParam(default=1)
    np_offset: float = fp.FloatParam(default=0)
    wg_length: float = fp.PositiveFloatParam(default=100)
    arm_spacing: float = fp.PositiveFloatParam(default=60)
    dc_length: float = fp.FloatParam(default=100)
    waveguide_type: WG.FWG.C = fp.WaveguideTypeParam(type=WG.FWG.C)
    pn_phase_shifter: fp.IDevice = fp.DeviceParam(type=PnPhaseShifter, port_count=2, pin_count=2, required=False)
    straight_waveguide: fp.IDevice = fp.DeviceParam(type=Straight, port_count=2, required=False)
    directional_coupler_left: fp.IDevice = fp.DeviceParam(type=DirectionalCouplerSBend, port_count=4, required=False)
    directional_coupler_right: fp.IDevice = fp.DeviceParam(type=DirectionalCouplerSBend, port_count=4, required=False)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4,default=["op_0", "op_1", "op_2", "op_3"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def _default_pn_phase_shifter(self):
        return PnPhaseShifter(
            name="ps", p_width=self.p_width, n_width=self.n_width, np_offset=self.np_offset,
            wg_length=self.wg_length-10, waveguide_type=self.waveguide_type,
            transform=fp.translate(5, 0)
        )
    def _default_straight_waveguide(self):
        return Straight(
            name="straight", waveguide_type=self.waveguide_type, length=self.wg_length, transform=fp.translate(0, -self.arm_spacing)
        )
    
    def _default_directional_coupler_left(self):
        return DirectionalCouplerSBend(
            name="dc_l", bend_radius=5,bend_degrees=27, waveguide_type=self.waveguide_type, transform=fp.translate(-self.dc_length, -self.arm_spacing / 2)
        )
    
    def _default_directional_coupler_right(self):
        return DirectionalCouplerSBend(
            name="dc_r", bend_radius=5,bend_degrees=27, waveguide_type=self.waveguide_type, transform=fp.translate(self.wg_length + self.dc_length, -self.arm_spacing / 2)
        )

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        # fmt: off

        waveguide_type = self.waveguide_type
        pn_phase_shifter = self.pn_phase_shifter.translated(-self.wg_length / 2, self.arm_spacing / 2)
        straight_waveguide = self.straight_waveguide.translated(-self.wg_length / 2, self.arm_spacing / 2)
        directional_coupler_left = self.directional_coupler_left.translated(-self.wg_length / 2, self.arm_spacing / 2)
        directional_coupler_right = self.directional_coupler_right.translated(-self.wg_length / 2, self.arm_spacing / 2)

        port_names = self.port_names
        ports += directional_coupler_left["op_0"].with_name(port_names[0])
        ports += directional_coupler_left["op_1"].with_name(port_names[1])
        ports += directional_coupler_right["op_2"].with_name(port_names[2])
        ports += directional_coupler_right["op_3"].with_name(port_names[3])

        insts += fp.Linked(
            link_type=waveguide_type,
            bend_factory=self.waveguide_type.BEND_EULER,
            links=[
                directional_coupler_left["op_3"] >> pn_phase_shifter["op_0"],
                directional_coupler_left["op_2"] >> straight_waveguide["op_0"],
                directional_coupler_right["op_0"] >> pn_phase_shifter["op_1"],
                directional_coupler_right["op_1"] >> straight_waveguide["op_1"],
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

    library += MZI()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
