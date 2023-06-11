import math
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Mapping, Optional, Sequence, Tuple, Type, cast

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt
from gpdk import all as pdk
from gpdk.technology import get_technology


@dataclass(eq=False)
class BendCosine(fp.IWaveguideLike, fp.PCell):
    degrees: float = fp.DegreeParam(default=90, min=-180, max=180, doc="Bend angle in degrees")
    radius_eff: float = fp.PositiveFloatParam(required=False, doc="Bend radius_eff")
    radius_min: Optional[float] = fp.PositiveFloatParam(required=False, doc="Bend radius_min")
    p: Optional[float] = fp.PositiveFloatParam(required=False, max=1, doc="Bend parameter")
    l_max: Optional[float] = fp.PositiveFloatParam(required=False, doc="Bend Lmax")
    waveguide_type: fp.IWaveguideType = fp.WaveguideTypeParam(doc="Waveguide parameters")
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=2, default=["op_0", "op_1"])

    def _default_radius_eff(self):
        if self.radius_min is None:
            return 10

    def _default_waveguide_type(self):
        return get_technology().WG.FWG.C.WIRE

    def __post_pcell_init__(self):
        assert self.radius_eff is not None or self.radius_min is not None, "either radius_eff or radius_min must be provided"

    @cached_property
    def raw_curve(self):
        radius_min = self.radius_min
        if radius_min is None:
            radius_min = self.radius_eff
        curve = fp.g.CosineBend(radius_min=radius_min, degrees=self.degrees, p=self.p, l_max=self.l_max)
        if self.radius_min is None and not fp.is_close(curve.radius_eff, self.radius_eff):
            curve = curve.scaled(self.radius_eff / curve.radius_eff)
        return curve

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        wg = self.waveguide_type(curve=self.raw_curve).with_ports(self.port_names)
        insts += wg
        ports += wg.ports
        return insts, elems, ports


@dataclass(frozen=True)
class CosineBendFactory(fpt.IBendWaveguideFactory):
    radius_min: float
    l_max: float
    waveguide_type: fpt.IWaveguideType = field(repr=False)

    def __call__(self, central_angle: float):
        bend = BendCosine(degrees=math.degrees(central_angle), radius_min=self.radius_min, l_max=self.l_max, waveguide_type=self.waveguide_type)
        return bend, bend.raw_curve.radius_eff, ("op_0", "op_1")


@dataclass(eq=False)
class LinkBetweenBase(fp.PCell, fpt.WaveguideBetween):
    start: fpt.IOwnedTerminal = fp.Param(type=fpt.IPort)
    end: fpt.IOwnedTerminal = fp.Param(type=fpt.IPort)
    waypoints: fpt.IWaypoints = fp.ListParam(default=(), immutable=True)
    waylines: fpt.IWaylines = fp.ListParam(default=(), immutable=True)
    link_type: fp.IWaveguideType = fp.Param()
    bend_factory: fp.IBendWaveguideFactory = fp.Param()

    def _default_link_type(self):
        TECH = get_technology()
        return TECH.WG.SWG.C.WIRE

    def _default_bend_factory(self):
        TECH = get_technology()
        return TECH.WG.FWG.C.WIRE.BEND_EULER

    @property
    def generated_link(self) -> fpt.IWaveguideBetween:
        link = fp.LinkBetween(
            self.start,
            self.end,
            waypoints=self.waypoints,
            waylines=self.waylines,
            link_type=self.link_type,
            bend_factory=self.bend_factory,
        )
        return link

    def build(self):
        inst_set, elem_set, port_set = super().build()

        inst_set += self.generated_link
        port_set += self.generated_link.ports

        return inst_set, elem_set, port_set

    def with_environment(self, **kwargs: Any):
        return self


class Linker:
    @dataclass(eq=False)
    class FWG_WIRE_CIRCULAR_WIRE(LinkBetweenBase):
        def _default_link_type(self):
            TECH = get_technology()
            return TECH.WG.FWG.C.WIRE

        def _default_bend_factory(self):
            TECH = get_technology()
            return TECH.WG.FWG.C.WIRE.BEND_CIRCULAR

    @dataclass(eq=False)
    class FWG_EXPANDED_EULER_WIRE(LinkBetweenBase):
        def _default_link_type(self):
            TECH = get_technology()
            return TECH.WG.FWG.C.EXPANDED

        def _default_bend_factory(self):
            TECH = get_technology()
            return TECH.WG.FWG.C.WIRE.BEND_EULER

    @dataclass(eq=False)
    class SWG_EXPANDED_COSINE_EXPANDED(LinkBetweenBase):
        def _default_link_type(self):
            TECH = get_technology()
            return TECH.WG.SWG.C.EXPANDED

        def _default_bend_factory(self):
            TECH = get_technology()
            wgt = TECH.WG.SWG.C.EXPANDED
            return CosineBendFactory(radius_min=wgt.cladding_width / 2 + 1, l_max=15, waveguide_type=wgt)


@dataclass(eq=False)
class Mzi(fp.PCell):
    dc1: fp.IDevice = fp.DeviceParam()
    dc2: fp.IDevice = fp.DeviceParam()
    ps: fp.IDevice = fp.DeviceParam()
    ps_offset: Tuple[float, float] = fp.Param()
    wg: fp.IDevice = fp.DeviceParam()
    wg_offset: Tuple[float, float] = fp.Param()
    dc_distance: float = fp.PositiveFloatParam(default=200)

    def _default_dc1(self):
        TECH = get_technology()
        return pdk.DirectionalCouplerBend(coupler_length=10, coupler_spacing=1.2, bend_radius=10, waveguide_type=TECH.WG.FWG.C.WIRE)

    def _default_dc2(self):
        TECH = get_technology()
        return pdk.DirectionalCouplerBend(coupler_length=10, coupler_spacing=1.2, bend_radius=10, waveguide_type=TECH.WG.FWG.C.WIRE)

    def _default_ps(self):
        TECH = get_technology()
        return pdk.PnPhaseShifter(wg_length=80, waveguide_type=TECH.WG.FWG.C.WIRE)

    def _default_ps_offset(self):
        return (-40, 50)

    def _default_wg(self):
        TECH = get_technology()
        return pdk.Straight(length=40, waveguide_type=TECH.WG.FWG.C.WIRE)

    def _default_wg_offset(self):
        return (-20, -50)

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        dc1 = self.dc1
        dc2 = self.dc2
        dc_distance = self.dc_distance
        ps = self.ps
        ps_offset = self.ps_offset
        wg = self.wg
        wg_offset = self.wg_offset

        dc1 = dc1.translated(-dc_distance / 2, 0)
        insts += dc1
        dc2 = dc2.translated(dc_distance / 2, 0)
        insts += dc2
        ps = ps.translated(*ps_offset)
        insts += ps
        wg = wg.translated(*wg_offset)
        insts += wg

        links = fp.create_links(
            link_type=TECH.WG.FWG.C.EXPANDED,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER,
            specs=[
                dc1["op_2"] >> wg["op_0"],
                wg["op_1"] >> dc2["op_1"],
                dc1["op_3"] >> ps["op_0"],
                ps["op_1"] >> dc2["op_0"],
            ],
        )
        insts += links

        ports += [
            dc1["op_0"].with_name("op_0"),
            dc1["op_1"].with_name("op_1"),
            dc2["op_2"].with_name("op_2"),
            dc2["op_3"].with_name("op_3"),
        ]

        return insts, elems, ports


@dataclass(eq=False)
class MziArray(fp.PCell):
    mzis: Sequence[Mzi] = fp.ListParam(default=(Mzi(),), immutable=True)
    rows: int = fp.PositiveIntParam(default=20)
    cols: int = fp.PositiveIntParam(default=20)

    period_x: float = fp.PositiveFloatParam(default=600)
    period_y: float = fp.PositiveFloatParam(default=200)

    offsets: Sequence[Tuple[float, float]] = fp.ListParam(default=((1, 1), (2, 2), (-1, 2), (-2, 1)), immutable=True)
    linkers: Sequence[Type[LinkBetweenBase]] = fp.ListParam(default=(fp.LinkBetween,), immutable=True)
    waypoints_candidates: Sequence[Any] = fp.ListParam(default=(fp.Offset(0, 0),), immutable=True)

    def build(self):
        insts, elems, ports = super().build()

        mzis = self.mzis
        rows = self.rows
        cols = self.cols
        period_x = self.period_x
        period_y = self.period_y
        offsets = self.offsets
        linkers = self.linkers
        waypoints_candidates = self.waypoints_candidates

        p = 0
        mzi_count = len(mzis)
        offset_count = len(offsets)
        linker_count = len(linkers)
        waypoints_candidates_count = len(waypoints_candidates)
        for i in range(rows):
            for j in range(cols):
                # choose mzi variant
                mzi = mzis[p % mzi_count]
                # get pseudo-random offset for mzi
                dx, dy = offsets[p % offset_count]
                # calculate mzi position
                tx = period_x * j + dx + (period_x / 2 if (i % 2 == 1) else 0)
                ty = period_y / 2 * math.sqrt(3) * i + dy
                # snap to grid to avoid 1nm gap and better performance
                tx = fp.snap_round(tx)
                ty = fp.snap_round(ty)
                # place mzi
                mzi_array = mzi.translated(tx, ty)
                insts += mzi_array, f"{i},{j}"
                # print(f"i:{i}, j:{j}, p:{p}, mzi:{p%mzi_count}")
                p += 1

        mapping = cast(Mapping[str, fp.ICellRef], insts)  # Just `mapping = insts` is OK, we cast here to help IDE typing
        for i in range(rows):
            for j in range(cols):
                linker = linkers[p % linker_count]
                if waypoints_candidates_count and i >= rows / 3 * 2 and j >= cols / 3 * 2:
                    waypoints = waypoints_candidates[p % waypoints_candidates_count]
                else:
                    waypoints = ()
                it = mapping[f"{i},{j}"]
                n = i % 2
                if n == 0:
                    if i == 0:
                        if j != cols - 1:
                            link = linker(start=it["op_2"], end=mapping[f"{i},{j + 1}"]["op_1"], waypoints=waypoints)
                            insts += link
                    if i != rows - 1:
                        link = linker(start=it["op_3"], end=mapping[f"{i+1},{j}"]["op_1"], waypoints=waypoints)
                        insts += link
                        if j != 0:
                            link = linker(start=mapping[f"{i+1},{j-1}"]["op_2"], end=it["op_0"], waypoints=waypoints)
                            insts += link
                    else:
                        if j != cols - 1:
                            link = linker(start=it["op_3"], end=mapping[f"{i},{j+1}"]["op_0"], waypoints=waypoints)
                            insts += link
                else:
                    if i != rows - 1:
                        link = linker(start=mapping[f"{i+1},{j}"]["op_2"], end=it["op_0"], waypoints=waypoints)
                        insts += link
                        if j != cols - 1:
                            link = linker(start=it["op_3"], end=mapping[f"{i+1},{j+1}"]["op_1"], waypoints=waypoints)
                            insts += link

                    if i == rows - 1:
                        if j != cols - 1:
                            link = linker(start=it["op_3"], end=mapping[f"{i},{j + 1}"]["op_0"], waypoints=waypoints)
                            insts += link
                p += 1

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from time import perf_counter
    from fnpcell import console
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================

    # ==== Warming up is optional, we can comment it out since the impact is not significant  ======
    console.info("Warming up ...")
    fp.export_gds(MziArray(rows=1, cols=1), file=fp.util.BytesIO())  # just warmup: module loading, initializing, ...,
    # ==== Warming up is optional, we can comment it out ======

    console.info("Start pure pcell layouting (about 2-3 minutes) ...")
    started_at = perf_counter()

    library += MziArray(
        rows=70,
        cols=70,
        period_x=1200,
        period_y=800,
        mzis=[  # mzi variants
            Mzi(
                dc1=pdk.DirectionalCouplerBend(coupler_length=12, coupler_spacing=1.2, bend_radius=10, waveguide_type=TECH.WG.FWG.C.WIRE),
                dc2=pdk.DirectionalCouplerBend(coupler_length=12, coupler_spacing=1.2, bend_radius=10, waveguide_type=TECH.WG.FWG.C.WIRE),
                dc_distance=200,
                ps=pdk.PnPhaseShifter(wg_length=80, waveguide_type=TECH.WG.FWG.C.WIRE),
                ps_offset=(-40, 50),
                wg=pdk.Straight(length=40, waveguide_type=TECH.WG.FWG.C.WIRE),
                wg_offset=(-20, -50),
            ),
            Mzi(
                dc1=pdk.DirectionalCouplerBend(coupler_length=12, coupler_spacing=1.2, bend_radius=10, waveguide_type=TECH.WG.SWG.C.WIRE),
                dc2=pdk.DirectionalCouplerBend(coupler_length=12, coupler_spacing=1.2, bend_radius=10, waveguide_type=TECH.WG.SWG.C.WIRE),
                dc_distance=200,
                ps=pdk.PnPhaseShifter(wg_length=80, waveguide_type=TECH.WG.FWG.C.WIRE),
                ps_offset=(-40, 50),
                wg=pdk.Straight(length=40, waveguide_type=TECH.WG.FWG.C.WIRE),
                wg_offset=(-20, -50),
            ),
            Mzi(
                dc1=pdk.DirectionalCouplerBend(coupler_length=12, coupler_spacing=1.2, bend_radius=10, waveguide_type=TECH.WG.MWG.C.WIRE),
                dc2=pdk.DirectionalCouplerBend(coupler_length=12, coupler_spacing=1.2, bend_radius=10, waveguide_type=TECH.WG.MWG.C.WIRE),
                dc_distance=200,
                ps=pdk.PnPhaseShifter(wg_length=80, waveguide_type=TECH.WG.FWG.C.WIRE),
                ps_offset=(-40, 50),
                wg=pdk.Straight(length=40, waveguide_type=TECH.WG.FWG.C.WIRE),
                wg_offset=(-20, -50),
            ),
        ],
        offsets=[(30, 20), (-10, 40), (-20, 30), (-40, 10), (-30, 20), (40, 10), (-40, -20)],  # pseudo-random offset to each mzi, more offsets, more randomness
        linkers=[Linker.FWG_WIRE_CIRCULAR_WIRE, Linker.FWG_EXPANDED_EULER_WIRE, Linker.SWG_EXPANDED_COSINE_EXPANDED],
        waypoints_candidates=[
            [fp.Offset(60, 100), fp.Offset(90, -50)],
            [fp.Offset(40, 200), fp.Offset(70, -50)],
            [fp.Offset(70, -100), fp.Offset(70, 50)],
            [fp.Offset(90, -200), fp.Offset(90, 50)],
        ],
    )

    # =============================================================
    console.info(f"Layouting elapsed time: {perf_counter() - started_at}s")
    fp.export_gds(library, file=gds_file)
    console.info(f"Total elapsed time: {perf_counter() - started_at}s")
    # fp.plot(library)
