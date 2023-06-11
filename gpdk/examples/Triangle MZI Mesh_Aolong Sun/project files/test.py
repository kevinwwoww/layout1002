from dataclasses import dataclass
from typing import Tuple, Mapping, cast

from fnpcell import all as fp
from gpdk.examples.mesh_mzi import MZI
from gpdk.technology import WG, get_technology
from gpdk.routing.extended.extended import Extended
from gpdk.technology.waveguide_factory import EulerBendFactory, CircularBendFactory
from gpdk.components.grating_coupler.grating_coupler import GratingCoupler
from gpdk.routing.comp_scan.comp_scan import CompScan,Block

@dataclass(eq=False)
class MZI_triangle_array(fp.PCell, band="C"):
    side_length: float = fp.PositiveFloatParam(default=400)
    dc_length: float = fp.FloatParam(default=100)
    arm_spacing: float = fp.FloatParam(default=60)
    wg_length: float = fp.FloatParam(default=100)
    gc_spacing: float = fp.FloatParam(default=50)
    waveguide_type: WG.FWG.C = fp.WaveguideTypeParam(type=WG.FWG.C)
    # link_type: WG.FWG.C.WIRE = fp.WaveguideTypeParam(type=WG.FWG.C.WIRE)
    MZI_unit: fp.IDevice = fp.DeviceParam(type=MZI, port_count=4, required=False)
    grating_coupler: fp.IDevice = fp.DeviceParam(type=GratingCoupler, port_count=1, required=False)
    port_names: fp.IPortOptions = fp.PortOptionsParam(count=8, default=["op_0", "op_1", "op_2", "op_3", "op_4", "op_5", "op_6", "op_7"])


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
        # link_type = self.link_type
        port_names = self.port_names

        row = 3
        column = 4

        for i in range(row):
            for j in range(column):
                if j % 2:
                    MZI = self.MZI_unit.translated(self.side_length * 2 * i / 2, self.side_length * j / 2 * (3) ** (0.5))
                else:
                    MZI = self.MZI_unit.translated(self.side_length / 2+ self.side_length * 2 * i / 2, self.side_length * j / 2 * (3) ** (0.5))
                insts += MZI, f"MZI_{i},{j}"

        for i in range(row):
            for j in range(column-1):
                if j % 2:
                    MZI_rotate_60 = self.MZI_unit.rotated(degrees=60).translated(self.side_length * ((-1) + 4 * i) / 4, self.side_length * (2*j+1) / 4 * (3) ** (0.5))
                else:
                    MZI_rotate_60 = self.MZI_unit.rotated(degrees=60).translated(self.side_length * ((1) + 4 * i) / 4, self.side_length * (2*j+1) / 4 * (3) ** (0.5))
                insts += MZI_rotate_60, f"MZI_60_{i},{j}"

        for i in range(row):
            for j in range(column-1):
                if j % 2:
                    MZI_rotate_120 = self.MZI_unit.rotated(degrees=120).translated(self.side_length * ((1)+4 * i) / 4, self.side_length * (2*j+1) / 4 * (3) ** (0.5))
                else:
                    MZI_rotate_120 = self.MZI_unit.rotated(degrees=120).translated(self.side_length * ((3)+4 * i) / 4, self.side_length * (2*j+1) / 4 * (3) ** (0.5))
                insts += MZI_rotate_120, f"MZI_120_{i},{j}"
        mzi = cast(Mapping[str, fp.ICellRef], insts)

        for i in range(column):
            for j in range(2):
                gc = self.grating_coupler.rotated(degrees=180).translated(mzi[f"MZI_0,0"]["op_1"].position[0]-300, -self.gc_spacing + (self.gc_spacing+10)*j+self.side_length*i / 2 * (3) ** (0.5))
                insts += gc, f"gc_left_{i},{j}"

        for i in range(column):
            for j in range(2):
                gc = self.grating_coupler.translated(mzi[f"MZI_0,1"]["op_1"].position[0]+self.side_length*row+250, -self.gc_spacing + (self.gc_spacing+10)*j+self.side_length*i / 2 * (3) ** (0.5))
                insts += gc, f"gc_right_{i},{j}"

        mzi = cast(Mapping[str, fp.ICellRef], insts)




        # mzi = cast(Mapping[str, fp.ICellRef], insts)

        # bot & top line
        for i in range(row-1):
            for j in range(column):
                if j == 0 :
                    link1 = fp.LinkBetween(
                        start = mzi[f"MZI_{i},{j}"]["op_2"],
                        end= mzi[f"MZI_{i+1},{j}"]["op_1"],
                        link_type=TECH.WG.FWG.C.WIRE,
                        bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER
                        )
                    insts += link1
                if j == column-1:
                    link2 = fp.LinkBetween(
                        start=mzi[f"MZI_{i},{j}"]["op_3"],
                        end=mzi[f"MZI_{i + 1},{j}"]["op_0"],
                        link_type=TECH.WG.FWG.C.WIRE,
                        bend_factory=TECH.WG.FWG.C.WIRE.BEND_EULER
                    )
                    insts += link2

        # 60&120 turning
        for i in range(row):
            for j in range(column - 1):
                if i < row:
                    link3 = fp.LinkBetween(
                        start=mzi[f"MZI_60_{i},{j}"]["op_2"],
                        end=mzi[f"MZI_120_{i},{j}"]["op_3"],
                        link_type=TECH.WG.FWG.C.WIRE,
                        bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR
                    )
                    insts += link3
                if i < row-1:
                    link4 = fp.LinkBetween(
                        start=mzi[f"MZI_60_{i+1},{j}"]["op_0"],
                        end=mzi[f"MZI_120_{i},{j}"]["op_1"],
                        link_type=TECH.WG.FWG.C.WIRE,
                        bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR
                    )
                    insts += link4

        for i in range(row):
            for j in range(column-1):
                if (j % 2==0) or  (j ==0) :
                    link5 = fp.LinkBetween(
                        start=mzi[f"MZI_60_{i},{j}"]["op_3"],
                        end=mzi[f"MZI_{i},{j+1}"]["op_2"],
                        link_type=TECH.WG.FWG.C.WIRE,
                        bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR
                    )
                    insts += link5
        for i in range(row-1):
            for j in range(column - 1):
                if j % 2==1:
                    link6 = fp.LinkBetween(
                        start=mzi[f"MZI_60_{i+1},{j}"]["op_3"],
                        end=mzi[f"MZI_{i},{j + 1}"]["op_2"],
                        link_type=TECH.WG.FWG.C.WIRE,
                        bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR
                    )
                    insts += link6


        for i in range(row-1):
            for j in range(column - 1):
                if j % 2:
                    link7 = fp.LinkBetween(
                        start=mzi[f"MZI_120_{i},{j}"]["op_2"],
                        end=mzi[f"MZI_{i},{j+1}"]["op_1"],
                        link_type=TECH.WG.FWG.C.WIRE,
                        bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR
                    )
                    insts += link7
                else:
                    link8 = fp.LinkBetween(
                        start=mzi[f"MZI_120_{i},{j}"]["op_2"],
                        end=mzi[f"MZI_{i+1},{j + 1}"]["op_1"],
                        link_type=TECH.WG.FWG.C.WIRE,
                        bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR
                    )
                    insts += link8

        for j in range(column-1):
            if j % 2:
                linkright = fp.LinkBetween(
                    start=mzi[f"MZI_120_{row-1},{j}"]["op_2"],
                    end=mzi[f"MZI_{row-1},{j + 1}"]["op_1"],
                    link_type=TECH.WG.FWG.C.WIRE,
                    bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR
                )
                insts += linkright

        for i in range(row):
            for j in range(column-1):
                link9 = fp.LinkBetween(
                    start=mzi[f"MZI_{i},{j}"]["op_0"],
                    end=mzi[f"MZI_60_{i},{j}"]["op_1"],
                    link_type=TECH.WG.FWG.C.WIRE,
                    bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR
                )
                insts += link9
                link10 = fp.LinkBetween(
                    start=mzi[f"MZI_{i},{j}"]["op_3"],
                    end=mzi[f"MZI_120_{i},{j}"]["op_0"],
                    link_type=TECH.WG.FWG.C.WIRE,
                    bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR
                )
                insts += link10




        for i in range(column-1):
            linkgcleft_1 = fp.LinkBetween(
                start=mzi[f"gc_left_{i},1"]["op_0"],
                end=mzi[f"MZI_60_0,{i}"]["op_0"],
                link_type=TECH.WG.FWG.C.WIRE,
                bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
            )
            insts += linkgcleft_1

        for i in range(column-1):
            if i % 2 ==0:
                linkgcleft_2 = fp.LinkBetween(
                    start=mzi[f"gc_left_{i+1},0"]["op_0"],
                    end=mzi[f"MZI_0,{i+1}"]["op_1"],
                    link_type=TECH.WG.FWG.C.WIRE,
                    bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
                    waypoints=[
                        fp.Waypoint(mzi[f"gc_left_{i+1},0"]["op_0"].position[0] + 50,
                                    mzi[f"MZI_0,{i+1}"]["op_1"].position[1],
                                    0)
                    ]

                )
                insts += linkgcleft_2
        for i in range(column-1):
            if i % 2 == 1:
                linkgcleft_3 = fp.LinkBetween(
                    start=mzi[f"gc_left_{i+1},0"]["op_0"],
                    end=mzi[f"MZI_60_0,{i}"]["op_3"],
                    link_type=TECH.WG.FWG.C.WIRE,
                    bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
                    waypoints=[
                        fp.Waypoint(mzi[f"gc_left_{i+1},0"]["op_0"].position[0] + 50,
                                    mzi[f"MZI_60_0,{i}"]["op_3"].position[1],
                                    90)
                    ]

                )
                insts += linkgcleft_3




        for i in range(column-1):
            linkgcright_1 = fp.LinkBetween(
                start=mzi[f"gc_right_{i},1"]["op_0"],
                end=mzi[f"MZI_120_{row-1},{i}"]["op_1"],
                link_type=TECH.WG.FWG.C.WIRE,
                bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
            )
            insts += linkgcright_1



        linkgcleft_top = fp.LinkBetween(
            start=mzi[f"gc_left_{column-1},1"]["op_0"],
            end=mzi[f"MZI_0,{column-1}"]["op_0"],
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
        )
        insts += linkgcleft_top
        linkgcleft_bot = fp.LinkBetween(
            start=mzi[f"gc_left_0,0"]["op_0"],
            end=mzi[f"MZI_0,0"]["op_1"],
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
            waypoints=[
                fp.Waypoint(mzi[f"gc_left_0,0"]["op_0"].position[0] + 50,
                            mzi[f"MZI_0,0"]["op_1"].position[1],
                            0)
            ]
        )
        insts += linkgcleft_bot
        linkgcright_top = fp.LinkBetween(
            start=mzi[f"gc_right_{column - 1},1"]["op_0"],
            end=mzi[f"MZI_{row-1},{column - 1}"]["op_3"],
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
        )
        insts += linkgcright_top
        linkgcright_bot = fp.LinkBetween(
            start=mzi[f"gc_right_0,0"]["op_0"],
            end=mzi[f"MZI_{row - 1},0"]["op_2"],
            link_type=TECH.WG.FWG.C.WIRE,
            bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
            waypoints=[
                fp.Waypoint(mzi[f"gc_right_0,0"]["op_0"].position[0]-50,
                            mzi[f"MZI_{row-1},0"]["op_2"].position[1],
                            -180)
            ]
        )
        insts += linkgcright_bot



        for i in range(column-1):
            if i%2:
                linkgcright_2 = fp.LinkBetween(
                    start=mzi[f"gc_right_{i+1},0"]["op_0"],
                    end=mzi[f"MZI_{row - 1},{i+1}"]["op_2"],
                    link_type=TECH.WG.FWG.C.WIRE,
                    bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
                    waypoints=[
                        fp.Waypoint(mzi[f"gc_right_{i+1},0"]["op_0"].position[0] - 50,
                                    mzi[f"MZI_{row - 1},{i+1}"]["op_2"].position[1],
                                    -180)
                    ]
                )
                insts += linkgcright_2
            else:
                linkgcright_3 = fp.LinkBetween(
                    start=mzi[f"gc_right_{i + 1},0"]["op_0"],
                    end=mzi[f"MZI_120_{row - 1},{i}"]["op_2"],
                    link_type=TECH.WG.FWG.C.WIRE,
                    bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
                    waypoints=[
                        fp.Waypoint(mzi[f"gc_right_{i + 1},0"]["op_0"].position[0] - 50,
                                    mzi[f"MZI_{row - 1},{i+1}"]["op_2"].position[1],
                                    -180)
                    ]

                )
                insts += linkgcright_3



        return insts, elems, ports

if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    library += MZI_triangle_array()

    fp.export_gds(library, file=gds_file)
    fp.plot(library)
