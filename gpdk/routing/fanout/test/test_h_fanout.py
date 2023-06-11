from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_h_fanout():
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off
    from gpdk.components.directional_coupler.directional_coupler_sbend import \
        DirectionalCouplerSBend
    from gpdk.components.mmi.mmi import Mmi
    from gpdk.technology.waveguide_factory import EulerBendFactory

    def bend_factories(waveguide_type: fp.IWaveguideType):
        if waveguide_type == TECH.WG.FWG.C.WIRE:
            return EulerBendFactory(radius_min=15, l_max=15, waveguide_type=waveguide_type)
        return waveguide_type.bend_factory

    library += fp.Device(
        name="h_fanout",
        content=[
            pdk.HFanout(
                name="dc_f0",
                device=Mmi(waveguide_type=TECH.WG.FWG.C.WIRE),  # for DEMO
                left_spacing=20,
                right_spacing=40,
                left_distance=50,
                right_distance=100,
                bend_degrees=30,
                device_left_ports=["op_0"],
                device_right_ports=["op_1"],
                # left_ports=["op_0", "op_1", "op_2", "op_3"],
            ),
            pdk.HFanout(
                name="dc_f1",
                device=DirectionalCouplerSBend(
                    name="0",
                    coupler_length=24,
                    coupler_spacing=2.8,
                    waveguide_type=TECH.WG.FWG.C.WIRE,
                ),  # for DEMO
                left_spacing=20,
                right_spacing=40,
                left_distance=50,
                right_distance=100,
                # bend_degrees=60,
                # radius_eff=7,
                device_left_ports=[
                    "op_0",
                ],
                device_right_ports=["op_2", "op_3"],
                left_waveguide_type=TECH.WG.SWG.C.WIRE,
                right_waveguide_type=TECH.WG.SWG.C.WIRE,
                # ports=["op_0", "op_1", "op_2", "op_3"],
            ).translated(0, 50),
            pdk.HFanout(
                name="dc_f1",
                device=DirectionalCouplerSBend(
                    name="0",
                    coupler_length=24,
                    coupler_spacing=2.8,
                    waveguide_type=TECH.WG.FWG.C.WIRE,
                ),  # for DEMO
                left_spacing=120,
                right_spacing=120,
                left_distance=100,
                right_distance=100,
                # bend_degrees=60,
                # radius_eff=7,
                bend_factories=bend_factories,
                device_left_ports=[
                    "op_0",
                ],
                device_right_ports=["op_2", "op_3"],
                left_waveguide_type=TECH.WG.SWG.C.WIRE,
                right_waveguide_type=TECH.WG.SWG.C.WIRE,
                # ports=["op_0", "op_1", "op_2", "op_3"],
            ).translated(0, 150),
            pdk.HFanout(
                name="dc_f1",
                device=Mmi(
                    waveguide_type=TECH.WG.FWG.C.WIRE,
                ),  # for DEMO
                left_spacing=120,
                right_spacing=120,
                left_distance=100,
                right_distance=100,
                # bend_degrees=60,
                # radius_eff=7,
                bend_factories=bend_factories,
                left_waveguide_type=TECH.WG.SWG.C.WIRE,
                right_waveguide_type=TECH.WG.SWG.C.WIRE,
                # ports=["op_0", "op_1", "op_2", "op_3"],
            ).translated(0, 250),
        ],
        ports=[],
    )

    # fmt: on
    # =============================================================
    # fp.plot(library)
    return library
