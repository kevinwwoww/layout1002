import math
from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from fpdk.components.mzm.mzm import Mzm
from fpdk.components.via.vias import Vias
from fpdk.technology import WG, get_technology


@dataclass(eq=False)
class TW_Mzm(fp.PCell, band="C"):
    """
    Attributes:
        modulator_length: defaults to 500
        delta: defaults to 60
        ground_width: defaults to 80
        signal_width: defaults to 10
        metal_spacing: defaults to 3
        delay: defaults to 0
        additional_length: defaults to 50
        pad_width: defaults to 50
        pad_length: defaults to 70
        taper_length: defaults to 60
        period_pad: defaults to 70
        waveguide_type: type of waveguide
        mzm: instance of `Mzm`, port_count=2, required=False
        port_names: defaults to ["elec_g1", "elec_g2", "elec_g3", "elec_s1", "elec_s2", "elec_g4", "elec_g5", "elec_g6", "elec_s3", "elec_s4"]

    Examples:
    ```python
    TECH = get_technology()
        mzm = TW_Mzm(modulator_length=500, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(mzm)
    ```
    ![TW_Mzm](images/TW_mzm.png)
    """

    modulator_length: float = fp.PositiveFloatParam(default=500)
    delta: float = fp.PositiveFloatParam(default=60)
    ground_width: float = fp.PositiveFloatParam(default=80)
    signal_width: float = fp.PositiveFloatParam(default=10)
    metal_spacing: float = fp.PositiveFloatParam(default=3.4)
    delay: float = fp.FloatParam(default=0)
    additional_length: float = fp.PositiveFloatParam(default=50)
    pad_width: float = fp.PositiveFloatParam(default=50)
    pad_length: float = fp.PositiveFloatParam(default=70)
    taper_length: float = fp.PositiveFloatParam(default=60)
    period_pad: float = fp.PositiveFloatParam(default=70)
    waveguide_type: WG.FWG.C = fp.WaveguideTypeParam(doc="Waveguide parameters")
    mzm: fp.IDevice = fp.DeviceParam(type=Mzm, port_count=2, required=False)
    port_names: fp.IPortOptions = fp.PortOptionsParam(
        count=10,
        default=(
            "elec_g1",
            "elec_g2",
            "elec_g3",
            "elec_s1",
            "elec_s2",
            "elec_g4",
            "elec_g5",
            "elec_g6",
            "elec_s3",
            "elec_s4",
        ),
    )

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off
        modulator_length = self.modulator_length
        delta = self.delta
        ground_width = self.ground_width
        signal_width = self.signal_width
        metal_spacing = self.metal_spacing
        delay = self.delay
        additional_length = self.additional_length
        pad_width =self.pad_width
        pad_length = self.pad_length
        taper_length = self.taper_length
        period_pad = self.period_pad
        waveguide_type = self.waveguide_type
        mzm = self.mzm
        port_names = self.port_names

        np_offset = 0.5*metal_spacing+0.3

        total_length = modulator_length + additional_length
        y_ground = (
            -delta
            + min(delay / 2.0, 0.0)
            - signal_width
            - 1.5 * metal_spacing
            - ground_width / 2.0
        )

        y_arm1_n = -delta + min(delay / 2.0, 0.0) - signal_width / 2.0 - metal_spacing / 2.0
        y_arm1_p = delay / 4.0 - signal_width / 2.0 - metal_spacing / 2.0
        y_arm2_n = delta + max(delay / 2.0, 0.0) - signal_width / 2.0 - metal_spacing / 2.0
        y_arm2_p = delta + max(delay / 2.0, 0.0) + ground_width / 2.0 + metal_spacing / 2.0
        arm2_n_width = 2 * delta + abs(delay / 2.0) - signal_width - 2 * metal_spacing
        phase_shifter_spacing = arm2_n_width+signal_width+2*metal_spacing

        mzm = mzm or Mzm(wg_length=modulator_length, phase_shifter_spacing=phase_shifter_spacing, np_offset=np_offset, splitter_wg_length=22.9,
                    waveguide_type=waveguide_type, transform=fp.translate(-modulator_length / 2, phase_shifter_spacing/2))
        insts += mzm

        # Metal
        ground = fp.el.Rect(width=total_length, height=ground_width, center=(0, y_ground), layer=TECH.LAYER.M1_DRW)
        elems += ground
        arm1_n = fp.el.Rect(width=total_length, height=signal_width, center=(0, y_arm1_n), layer=TECH.LAYER.M1_DRW)
        elems += arm1_n
        arm1_p = fp.el.Rect(width=total_length, height=arm2_n_width, center=(0, y_arm1_p), layer=TECH.LAYER.M1_DRW)
        elems += arm1_p
        arm2_n = fp.el.Rect(width=total_length, height=signal_width, center=(0, y_arm2_n), layer=TECH.LAYER.M1_DRW)
        elems += arm2_n
        arm2_p = fp.el.Rect(width=total_length, height=ground_width, center=(0, y_arm2_p), layer=TECH.LAYER.M1_DRW)
        elems += arm2_p

        # fmt: on
        # Taper
        taper_ground = fp.el.Polygon(
            [
                (
                    -(total_length / 2.0 + taper_length),
                    y_arm1_p - 2 * period_pad + pad_width / 2.0,
                ),
                (
                    -(total_length / 2.0 + taper_length),
                    y_arm1_p - 2 * period_pad - pad_width / 2.0,
                ),
                (-total_length / 2.0, y_ground - ground_width / 2.0),
                (-total_length / 2.0, y_ground + ground_width / 2.0),
            ],
            layer=TECH.LAYER.M1_DRW,
        )
        elems += taper_ground
        elems += taper_ground.h_mirrored()
        taper_arm1_n = fp.el.Polygon(
            [
                (
                    -(total_length / 2.0 + taper_length),
                    y_arm1_p - period_pad + pad_width / 2.0,
                ),
                (
                    -(total_length / 2.0 + taper_length),
                    y_arm1_p - period_pad - pad_width / 2.0,
                ),
                (-total_length / 2.0, y_arm1_n - signal_width / 2.0),
                (-total_length / 2.0, y_arm1_n + signal_width / 2.0),
            ],
            layer=TECH.LAYER.M1_DRW,
        )
        elems += taper_arm1_n
        elems += taper_arm1_n.h_mirrored()
        taper_arm1_p = fp.el.Line(
            length=taper_length,
            stroke_width=pad_width,
            final_stroke_width=arm2_n_width,
            layer=TECH.LAYER.M1_DRW,
            origin=(-(total_length / 2 + taper_length), y_arm1_p),
        )
        elems += taper_arm1_p
        elems += taper_arm1_p.h_mirrored()
        taper_arm2_n = fp.el.Polygon(
            [
                (
                    -(total_length / 2.0 + taper_length),
                    y_arm1_p + period_pad + pad_width / 2.0,
                ),
                (
                    -(total_length / 2.0 + taper_length),
                    y_arm1_p + period_pad - pad_width / 2.0,
                ),
                (-total_length / 2.0, y_arm2_n - signal_width / 2.0),
                (-total_length / 2.0, y_arm2_n + signal_width / 2.0),
            ],
            layer=TECH.LAYER.M1_DRW,
        )
        elems += taper_arm2_n
        elems += taper_arm2_n.h_mirrored()
        taper_arm2_p = fp.el.Polygon(
            [
                (
                    -(total_length / 2.0 + taper_length),
                    y_arm1_p + 2 * period_pad + pad_width / 2.0,
                ),
                (
                    -(total_length / 2.0 + taper_length),
                    y_arm1_p + 2 * period_pad - pad_width / 2.0,
                ),
                (-total_length / 2.0, y_arm2_p - ground_width / 2.0),
                (-total_length / 2.0, y_arm2_p + ground_width / 2.0),
            ],
            layer=TECH.LAYER.M1_DRW,
        )
        elems += taper_arm2_p
        elems += taper_arm2_p.h_mirrored()

        for i in range(-2, 3):
            origin = (
                -(total_length / 2.0 + taper_length + pad_length / 2.0),
                y_arm1_p + i * period_pad,
            )
            origin_h_mirror = (
                (total_length / 2.0 + taper_length + pad_length / 2.0),
                y_arm1_p + i * period_pad,
            )
            left_pad_m1 = fp.el.Rect(width=pad_length, height=pad_width, center=origin, layer=TECH.LAYER.M1_DRW)
            elems += left_pad_m1
            right_pad_m1 = left_pad_m1.h_mirrored(x=0)
            elems += right_pad_m1
            left_pad_m2 = fp.el.Rect(width=pad_length, height=pad_width, center=origin, layer=TECH.LAYER.M2_DRW)
            elems += left_pad_m2
            right_pad_m2 = left_pad_m2.h_mirrored(x=0)
            elems += right_pad_m2
            left_pad_mt = fp.el.Rect(width=pad_length, height=pad_width, center=origin, layer=TECH.LAYER.MT_DRW)
            elems += left_pad_mt
            right_pad_mt = left_pad_mt.h_mirrored(x=0)
            elems += right_pad_mt

            left_vias1 = Vias(
                width=pad_length,
                height=pad_width,
                top_layer=TECH.LAYER.M2_DRW,
                via_layer=TECH.LAYER.VIA1_DRW,
                bottom_layer=TECH.LAYER.M1_DRW,
                transform=fp.translate(*origin),
            )
            insts += left_vias1
            right_vias1 = left_vias1.h_mirrored(x=0)
            insts += right_vias1

            left_vias2 = Vias(
                width=pad_length,
                height=pad_width,
                top_layer=TECH.LAYER.MT_DRW,
                via_layer=TECH.LAYER.VIA2_DRW,
                bottom_layer=TECH.LAYER.M2_DRW,
                transform=fp.translate(*origin),
            )
            insts += left_vias2
            right_vias2 = left_vias2.h_mirrored(x=0)
            insts += right_vias2

            left_pad_pass_mt = fp.el.Rect(
                width=pad_length - 5,
                height=pad_width - 5,
                center=origin,
                layer=TECH.LAYER.PASS_MT,
            )
            elems += left_pad_pass_mt
            right_pad_pass_mt = left_pad_pass_mt.h_mirrored(x=0)
            elems += right_pad_pass_mt
            ports += fp.Pin(name=port_names[i + 2], position=origin, orientation=math.pi, shape=left_pad_pass_mt.shape, metal_line_type=TECH.METAL.M1.W20)
            ports += fp.Pin(name=port_names[i + 7], position=origin_h_mirror, orientation=0, shape=right_pad_pass_mt.shape, metal_line_type=TECH.METAL.MT.W20)

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from fpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += TW_Mzm()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
