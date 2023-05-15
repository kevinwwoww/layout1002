import math
from dataclasses import dataclass
from typing import Tuple

from fnpcell import all as fp
from fpdk.technology import WG, get_technology


@dataclass(eq=False)
class PnPhaseShifter(fp.PCell):
    """
    Attributes:
        p_width: defaults to 1
        n_width: defaults to 1
        np_offset: defaults to 0
        wg_length: defaults to 25
        waveguide_type: type of waveguide
        port_names: defaults to ["op_0", "op_1", "ep_0", "ep_1"]

    Examples:
    ```python
    TECH = get_technology()
        ps = PnPhaseShifter(name="p1", wg_length=200, waveguide_type=TECH.WG.FWG.C.WIRE)
    fp.plot(ps)
    ```
    ![PnPhaseShifter](images/pn_phase_shifter.png)
    """

    p_width: float = fp.PositiveFloatParam(default=1)
    n_width: float = fp.PositiveFloatParam(default=1)
    np_offset: float = fp.FloatParam(default=0)
    wg_length: float = fp.PositiveFloatParam(default=25)
    waveguide_type: WG.FWG.C = fp.WaveguideTypeParam(type=WG.FWG.C)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=4, default=["op_0", "op_1", "ep_0", "ep_1"])

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        # fmt: off
        # p_width = self.p_width # TODO
        n_width = self.n_width
        np_offset = self.np_offset
        wg_length = self.wg_length
        waveguide_type =self.waveguide_type
        port_names = self.port_names

        LAYER = TECH.LAYER
        si_etch2_layer = LAYER.SWG_COR
        slab_width = 10
        vc_incl = 2
        taper_length = 5
        taper_small_end = 0.2
        taper_big_end = 2
        x0 = wg_length / 2
        y0 = 0

        wg = waveguide_type(
            curve=fp.g.Line(
                length=wg_length + taper_length * 2,
                anchor=fp.Anchor.CENTER,
                origin=(x0, y0),
            ),
        ).with_name("wg")
        insts += wg
        ports += wg["op_0"].with_name(port_names[0])
        ports += wg["op_1"].with_name(port_names[1])
        # SWG Layer
        rect = fp.el.Rect(width=wg_length, height=slab_width * 2, center=(x0, 0), layer=si_etch2_layer)
        taper1 = fp.el.Line(
            length=taper_length,
            stroke_width=taper_small_end,
            final_stroke_width=taper_big_end,
            layer=si_etch2_layer,
            anchor=fp.Anchor.END,
            origin=(0, 0),
        )
        taper2 = fp.el.Line(
            length=taper_length,
            stroke_width=taper_big_end,
            final_stroke_width=taper_small_end,
            layer=si_etch2_layer,
            anchor=fp.Anchor.START,
            origin=(wg_length, 0),
        )
        elems += rect
        elems += taper1
        elems += taper2

        # N_DRW Layer
        n_rect = fp.el.Rect(
            width=wg_length,
            height=slab_width - np_offset,
            center=(x0, (slab_width - np_offset) / 2),
            layer=LAYER.N_DRW,
        )
        elems += n_rect
        # P_DRW Layer
        p_rect = fp.el.Rect(
            width=wg_length,
            height=slab_width - np_offset,
            center=(x0, -(slab_width - np_offset) / 2),
            layer=LAYER.P_DRW,
        )
        elems += p_rect
        # NPP_DRW Layer
        npp_rect = fp.el.Rect(
            width=wg_length,
            height=slab_width - np_offset - n_width,
            center=(x0, (slab_width - np_offset + n_width) / 2),
            layer=LAYER.NPP_DRW,
        )
        elems += npp_rect
        # PPP_DRW Layer
        ppp_rect = fp.el.Rect(
            width=wg_length,
            height=slab_width - np_offset - n_width,
            center=(x0, -(slab_width - np_offset + n_width) / 2),
            layer=LAYER.PPP_DRW,
        )
        elems += ppp_rect

        # CONT_DRW Layer
        cont_x0 = (wg_length + vc_incl) / 2
        cont_rect1_y0 = (slab_width + np_offset + n_width + 1) / 2
        cont_rect2_y0 = -(slab_width - np_offset + n_width + 1) / 2
        cont_rect1 = fp.el.Rect(
            width=wg_length - vc_incl,
            height=slab_width - vc_incl - np_offset - n_width - vc_incl - 1,
            center=(cont_x0, cont_rect1_y0),
            layer=LAYER.CONT_DRW,
        )
        elems += cont_rect1
        cont_rect2 = fp.el.Rect(
            width=wg_length - vc_incl,
            height=slab_width + np_offset - n_width - 2 * vc_incl - 1,
            center=(cont_x0, cont_rect2_y0),
            layer=LAYER.CONT_DRW,
        )
        elems += cont_rect2

        # M1 Layer
        m1_rect1 = fp.el.Rect(
            width=wg_length,
            height=3 * slab_width - np_offset - n_width - 1,
            center=(wg_length / 2, (3 * slab_width + np_offset + n_width + 1) / 2),
            layer=LAYER.CONT_DRW,
        )
        m1_rect2 = fp.el.Rect(
            width=wg_length,
            height=3 * slab_width + np_offset - n_width - 1,
            center=(wg_length / 2, (-3 * slab_width + np_offset - n_width - 1) / 2),
            layer=LAYER.CONT_DRW,
        )
        m1_rect3 = fp.el.Rect(
            width=slab_width,
            height=slab_width,
            center=(slab_width / 2, slab_width * 5 / 2),
            layer=LAYER.CONT_DRW,
        )
        m1_rect4 = fp.el.Rect(
            width=slab_width,
            height=slab_width,
            center=(slab_width / 2, -5 * slab_width / 2),
            layer=LAYER.CONT_DRW,
        )
        elems += m1_rect1
        elems += m1_rect2
        elems += m1_rect3
        elems += m1_rect4
        ports += fp.Pin(name=port_names[2], position=(slab_width / 2, slab_width * 5 / 2), orientation=math.pi/2,shape=m1_rect3.shape, metal_line_type=TECH.METAL.M1.W20)
        ports += fp.Pin(name=port_names[3], position=(slab_width / 2, -slab_width * 5 / 2), orientation=-math.pi/2,shape=m1_rect4.shape, metal_line_type=TECH.METAL.M1.W20)

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from fpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += PnPhaseShifter()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
