from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import WG
from layout01.technology import get_technology


@dataclass(eq=False)
class Circuit01(fp.PCell):
    gc_spacing: float = fp.FloatParam(default=90, min=0)
    ring_radius: float = fp.FloatParam(default=10, min=0)
    bend_degrees: float = fp.DegreeParam(default=30, min=-60, max=60, invalid=[0])
    swg_spacing: float = fp.FloatParam(default=30, min=0)
    swg_length: float = fp.FloatParam(default=10, min=0)
    fwg_type: WG.FWG.C = fp.WaveguideTypeParam(type=WG.FWG.C, default=get_technology().WG.FWG.C.WIRE)
    swg_type: WG.SWG.C = fp.WaveguideTypeParam(type=WG.SWG.C, default=get_technology().WG.SWG.C.WIRE)
    mwg_type: WG.MWG.C = fp.WaveguideTypeParam(type=WG.MWG.C, default=get_technology().WG.MWG.C.WIRE)
    transform: fp.Affine2D = fp.TransformParam()
    dc_0: fp.IDevice = fp.DeviceParam(type=pdk.DirectionalCouplerSBend, port_count=4, required=False)
    dc_1: fp.IDevice = fp.DeviceParam(type=pdk.DirectionalCouplerSBend, port_count=4, required=False)
    gc_0: fp.IDevice = fp.DeviceParam(type=pdk.GratingCoupler, port_count=1, required=False)
    gc_1: fp.IDevice = fp.DeviceParam(type=pdk.GratingCoupler, port_count=1, required=False)
    gc_2: fp.IDevice = fp.DeviceParam(type=pdk.GratingCoupler, port_count=1, required=False)
    gc_3: fp.IDevice = fp.DeviceParam(type=pdk.GratingCoupler, port_count=1, required=False)

    def build(self):
        insts, elems, ports = super().build()
        gc_spacing = self.gc_spacing
        fwg_type = self.fwg_type
        swg_type = self.swg_type
        mwg_type = self.mwg_type
        bend_degrees = self.bend_degrees
        swg_spacing = self.swg_spacing
        swg_length = self.swg_length

        fwg_ring_filter = pdk.RingFilter(name="f0", ring_radius=self.ring_radius, waveguide_type=fwg_type)

        ring_port_spacing = fp.distance_between(fwg_ring_filter["op_0"].position, fwg_ring_filter["op_1"].position)

        dc_0_fanout = pdk.HFanout(
            name="dc_f0",
            device=(
                self.dc_0
                or pdk.DirectionalCouplerSBend(
                    name="0",
                    waveguide_type=fwg_type,
                )
            ),
            left_spacing=swg_spacing,
            right_spacing=ring_port_spacing,
            bend_degrees=bend_degrees,
            device_left_ports=["op_0", "op_1"],
            device_right_ports=["op_2", "op_3"],
        )

        dc_1_fanout = pdk.HFanout(
            name="dc_f1",
            device=(
                self.dc_1
                or pdk.DirectionalCouplerSBend(
                    name="1",
                    waveguide_type=fwg_type,
                )
            ),
            left_spacing=ring_port_spacing,
            device_left_ports=["op_0", "op_1"],
            right_spacing=swg_spacing,
            device_right_ports=["op_2", "op_3"],
            bend_degrees=bend_degrees,
        )

        short_transition_length = 5.0
        fwg2swg_0 = pdk.FWG2SWGTransition(name="0", fwg_type=fwg_type, swg_type=swg_type, length=short_transition_length)
        fwg2swg_1 = pdk.FWG2SWGTransition(name="1", fwg_type=fwg_type, swg_type=swg_type, length=short_transition_length)
        fwg2swg_3 = pdk.FWG2SWGTransition(name="3", fwg_type=fwg_type, swg_type=swg_type, length=short_transition_length)
        fwg2swg_2 = pdk.FWG2SWGTransition(name="2", fwg_type=fwg_type, swg_type=swg_type, length=short_transition_length)

        ring_connected = fp.Connected(
            name="Connected_1",
            joints=[
                fwg_ring_filter["op_0"] <= dc_0_fanout["op_3"],
                dc_0_fanout["op_0"] <= fwg2swg_0["op_0"],
                #
                fwg_ring_filter["op_1"] <= dc_0_fanout["op_2"],
                dc_0_fanout["op_1"] <= fwg2swg_1["op_0"],
                #
                fwg_ring_filter["op_3"] <= dc_1_fanout["op_0"],
                dc_1_fanout["op_3"] <= fwg2swg_3["op_0"],
                #
                fwg_ring_filter["op_2"] <= dc_1_fanout["op_1"],
                dc_1_fanout["op_2"] <= fwg2swg_2["op_0"],
            ],
            ports=[
                fwg2swg_0["op_1"].with_name("op_0"),
                fwg2swg_1["op_1"].with_name("op_1"),
                fwg2swg_2["op_1"].with_name("op_2"),
                fwg2swg_3["op_1"].with_name("op_3"),
            ],
        )

        s_0 = pdk.Straight(name="0", length=swg_length, waveguide_type=swg_type)
        s_1 = pdk.Straight(name="1", length=swg_length, waveguide_type=swg_type)
        s_2 = pdk.Straight(name="2", length=swg_length, waveguide_type=swg_type)
        s_3 = pdk.Straight(name="3", length=swg_length, waveguide_type=swg_type)

        swg2mwg_0 = pdk.SWG2MWGTransition(name="0", swg_type=swg_type, mwg_type=mwg_type)
        swg2mwg_1 = pdk.SWG2MWGTransition(name="1", swg_type=swg_type, mwg_type=mwg_type)
        swg2mwg_2 = pdk.SWG2MWGTransition(name="2", swg_type=swg_type, mwg_type=mwg_type)
        swg2mwg_3 = pdk.SWG2MWGTransition(name="3", swg_type=swg_type, mwg_type=mwg_type)

        ring_connected = fp.Connected(
            name="Connected_2",
            joints=[
                ring_connected["op_0"] <= s_0["op_1"],
                s_0["op_0"] <= swg2mwg_0["op_0"],
                #
                ring_connected["op_1"] <= s_1["op_1"],
                s_1["op_0"] <= swg2mwg_1["op_0"],
                #
                ring_connected["op_3"] <= s_3["op_0"],
                s_3["op_1"] <= swg2mwg_3["op_0"],
                #
                ring_connected["op_2"] <= s_2["op_0"],
                s_2["op_1"] <= swg2mwg_2["op_0"],
            ],
            ports=[
                swg2mwg_0["op_1"].with_name("op_0"),
                swg2mwg_1["op_1"].with_name("op_1"),
                swg2mwg_2["op_1"].with_name("op_2"),
                swg2mwg_3["op_1"].with_name("op_3"),
            ],
        )

        mwg_gc_0 = self.gc_0 or pdk.GratingCoupler(name="0", waveguide_type=mwg_type)
        mwg_gc_1 = self.gc_1 or pdk.GratingCoupler(name="1", waveguide_type=mwg_type)
        mwg_gc_2 = self.gc_2 or pdk.GratingCoupler(name="2", waveguide_type=mwg_type)
        mwg_gc_3 = self.gc_3 or pdk.GratingCoupler(name="3", waveguide_type=mwg_type)

        swg2mwg_spacing = fp.distance_between(ring_connected["op_0"].position, ring_connected["op_1"].position)

        left_sbend_pair = pdk.SBendCircularPair(left_spacing=gc_spacing, right_spacing=swg2mwg_spacing, bend_degrees=bend_degrees, waveguide_type=mwg_type)
        right_sbend_pair = pdk.SBendCircularPair(left_spacing=swg2mwg_spacing, right_spacing=gc_spacing, bend_degrees=bend_degrees, waveguide_type=mwg_type)

        ring_connected = fp.Connected(
            name="Connected_3",
            joints=[
                ring_connected["op_0"] <= left_sbend_pair["op_3"],
                left_sbend_pair["op_0"] <= mwg_gc_0["op_0"],
                #
                ring_connected["op_1"] <= left_sbend_pair["op_2"],
                left_sbend_pair["op_1"] <= mwg_gc_1["op_0"],
                #
                ring_connected["op_2"] <= right_sbend_pair["op_1"],
                right_sbend_pair["op_2"] <= mwg_gc_2["op_0"],
                #
                ring_connected["op_3"] <= right_sbend_pair["op_0"],
                right_sbend_pair["op_3"] <= mwg_gc_3["op_0"],
            ],
            ports=[],
        )
        insts += ring_connected
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    fwg_type = TECH.WG.FWG.C.WIRE

    library += Circuit01(
        name="01",
        gc_spacing=100,
        ring_radius=50,
        swg_spacing=30,
        swg_length=50,
        fwg_type=fwg_type,
        swg_type=TECH.WG.SWG.C.WIRE,
        mwg_type=TECH.WG.MWG.C.WIRE,
        dc_0=pdk.DirectionalCouplerSBend(
            name="0",
            coupler_length=24,
            coupler_spacing=2.8,  # just for DEMO
            bend_radius=10,
            waveguide_type=fwg_type,
        ),
        # dc_1=pdk.Straight(name="t", length=100, waveguide_type=TECH.WG.FWG.C.WIRE),  # DeviceParam(type=...) DEMO
        gc_2=pdk.GratingCoupler(name="m2", length=50, waveguide_type=TECH.WG.MWG.C.WIRE),  # just for DEMO
    )

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
