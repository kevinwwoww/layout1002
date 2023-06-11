from dataclasses import dataclass
from typing import Dict, Mapping, cast
from fnpcell import all as fp

from gpdk.technology import get_technology
from gpdk import all as pdk_all

try:
    from gpdk import func_all as func_all
except:
    pass

@fp.pcell_class()
@dataclass(eq=False)
class example_demultiplexer21(fp.PCell):

    instance_naming_table: Mapping[fp.ICellRef, str] = fp.MappingParam(default_factory=dict, frozen=True).as_field(compare=False)
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        instance_naming_table = cast(Dict[fp.ICellRef, str], self.instance_naming_table)

        DirectionalCouplerBend_1_temp = pdk_all.DirectionalCouplerBend(
            coupler_spacing=1.5,
            coupler_length=3.0,
            bend_radius=25.0,
            straight_after_bend=6.0,
            waveguide_type=TECH.WG.MWG.C.WIRE
        )

        Fixed_Edge_Coupler_1_temp = pdk_all.Fixed_Edge_Coupler().rotated(degrees=0.00)

        Fixed_Edge_Coupler_2_temp = pdk_all.Fixed_Edge_Coupler().rotated(degrees=0.00)

        DirectionalCouplerBend_2_temp = pdk_all.DirectionalCouplerBend(
            coupler_spacing=1.5,
            coupler_length=3.0,
            bend_radius=25.0,
            straight_after_bend=6.0,
            waveguide_type=TECH.WG.MWG.C.WIRE
        ).rotated(degrees=0.00)

        DirectionalCouplerBend_3_temp = pdk_all.DirectionalCouplerBend(
            coupler_spacing=1.5,
            coupler_length=31.0,
            bend_radius=25.0,
            straight_after_bend=6.0,
            waveguide_type=TECH.WG.MWG.C.WIRE
        ).rotated(degrees=0.00)

        Fixed_Terminator_TE_1550_1_temp = pdk_all.Fixed_Terminator_TE_1550(
            length=30.0,
            waveguide_type=TECH.WG.MWG.C.WIRE
        )

        Fixed_Photo_Detector_1_temp = pdk_all.Fixed_Photo_Detector().h_mirrored(x=0)

        DirectionalCouplerBend_4_temp = pdk_all.DirectionalCouplerBend(
            coupler_spacing=1.5,
            coupler_length=18.0,
            bend_radius=25.0,
            straight_after_bend=6.0,
            waveguide_type=TECH.WG.MWG.C.WIRE
        ).rotated(degrees=0.00)

        Fixed_Photo_Detector_2_temp = pdk_all.Fixed_Photo_Detector().h_mirrored(x=0)

        Fixed_Terminator_TE_1550_2_temp = pdk_all.Fixed_Terminator_TE_1550(
            length=30.0,
            waveguide_type=TECH.WG.MWG.C.WIRE
        ).rotated(degrees=-180).h_mirrored(x=0)

        Fixed_Photo_Detector_3_temp = pdk_all.Fixed_Photo_Detector().h_mirrored(x=0)

        Fixed_Photo_Detector_4_temp = pdk_all.Fixed_Photo_Detector().h_mirrored(x=0)

        DirectionalCouplerBend_5_temp = pdk_all.DirectionalCouplerBend(
            coupler_spacing=1.5,
            coupler_length=31.0,
            bend_radius=25.0,
            straight_after_bend=6.0,
            waveguide_type=TECH.WG.MWG.C.WIRE
        ).rotated(degrees=0.00)

        DirectionalCouplerBend_6_temp = pdk_all.DirectionalCouplerBend(
            coupler_spacing=1.5,
            coupler_length=31.0,
            bend_radius=25.0,
            straight_after_bend=6.0,
            waveguide_type=TECH.WG.MWG.C.WIRE
        ).rotated(degrees=0.00)

        DirectionalCouplerBend_7_temp = pdk_all.DirectionalCouplerBend(
            coupler_spacing=1.5,
            coupler_length=3.0,
            bend_radius=25.0,
            straight_after_bend=6.0,
            waveguide_type=TECH.WG.MWG.C.WIRE
        ).rotated(degrees=0.00)



        Fixed_Terminator_TE_1550_1_entity = fp.place(Fixed_Terminator_TE_1550_1_temp, "op_0", at=fp.Waypoint(600.0000, -500.0000, 0))
        DirectionalCouplerBend_1_entity = DirectionalCouplerBend_1_temp.translated(351.4007, 328.5990)
        Fixed_Edge_Coupler_1_entity = Fixed_Edge_Coupler_1_temp.translated(-100.0000, -150.0000)
        Fixed_Edge_Coupler_2_entity = Fixed_Edge_Coupler_2_temp.translated(-100.0000, 150.0000)
        DirectionalCouplerBend_2_entity = DirectionalCouplerBend_2_temp.translated(600.0000, 0.0000)
        DirectionalCouplerBend_3_entity = DirectionalCouplerBend_3_temp.translated(508.4000, -319.9936)
        Fixed_Photo_Detector_1_entity = Fixed_Photo_Detector_1_temp.translated(-100.0000, -400.0000)
        DirectionalCouplerBend_4_entity = DirectionalCouplerBend_4_temp.translated(400.0000, 0.0000)
        Fixed_Photo_Detector_2_entity = Fixed_Photo_Detector_2_temp.translated(-100.0000, -250.0000)
        Fixed_Terminator_TE_1550_2_entity = Fixed_Terminator_TE_1550_2_temp.translated(600.0000, 607.6074)
        Fixed_Photo_Detector_3_entity = Fixed_Photo_Detector_3_temp.translated(-100.0000, 250.0000)
        Fixed_Photo_Detector_4_entity = Fixed_Photo_Detector_4_temp.translated(-100.0000, 400.0000)
        DirectionalCouplerBend_5_entity = DirectionalCouplerBend_5_temp.translated(511.4007, 328.5990)
        DirectionalCouplerBend_6_entity = DirectionalCouplerBend_6_temp.translated(200.0000, 0.0000)
        DirectionalCouplerBend_7_entity = DirectionalCouplerBend_7_temp.translated(348.4000, -322.9942)

        instance_naming_table[DirectionalCouplerBend_1_entity] = "U1019X"
        insts += DirectionalCouplerBend_1_entity
        instance_naming_table[Fixed_Edge_Coupler_1_entity] = "U1020X"
        insts += Fixed_Edge_Coupler_1_entity
        instance_naming_table[Fixed_Edge_Coupler_2_entity] = "U1021X"
        insts += Fixed_Edge_Coupler_2_entity
        instance_naming_table[DirectionalCouplerBend_2_entity] = "U1022X"
        insts += DirectionalCouplerBend_2_entity
        instance_naming_table[DirectionalCouplerBend_3_entity] = "U1023X"
        insts += DirectionalCouplerBend_3_entity
        instance_naming_table[Fixed_Terminator_TE_1550_1_entity] = "U1024X"
        insts += Fixed_Terminator_TE_1550_1_entity
        instance_naming_table[Fixed_Photo_Detector_1_entity] = "U1025X"
        insts += Fixed_Photo_Detector_1_entity
        instance_naming_table[DirectionalCouplerBend_4_entity] = "U1026X"
        insts += DirectionalCouplerBend_4_entity
        instance_naming_table[Fixed_Photo_Detector_2_entity] = "U1027X"
        insts += Fixed_Photo_Detector_2_entity
        instance_naming_table[Fixed_Terminator_TE_1550_2_entity] = "U1028X"
        insts += Fixed_Terminator_TE_1550_2_entity
        instance_naming_table[Fixed_Photo_Detector_3_entity] = "U1029X"
        insts += Fixed_Photo_Detector_3_entity
        instance_naming_table[Fixed_Photo_Detector_4_entity] = "U1030X"
        insts += Fixed_Photo_Detector_4_entity
        instance_naming_table[DirectionalCouplerBend_5_entity] = "U1031X"
        insts += DirectionalCouplerBend_5_entity
        instance_naming_table[DirectionalCouplerBend_6_entity] = "U1032X"
        insts += DirectionalCouplerBend_6_entity
        instance_naming_table[DirectionalCouplerBend_7_entity] = "U1033X"
        insts += DirectionalCouplerBend_7_entity

        links = fp.create_links(
            specs=[
                fp.LinkBetween(
                    start=Fixed_Edge_Coupler_1_entity["op_0"],
                    end=DirectionalCouplerBend_6_entity["op_1"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER), 
                fp.LinkBetween(
                    start=Fixed_Edge_Coupler_2_entity["op_0"],
                    end=DirectionalCouplerBend_6_entity["op_0"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_4_entity["op_3"],
                    end=DirectionalCouplerBend_2_entity["op_0"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_4_entity["op_2"],
                    end=DirectionalCouplerBend_2_entity["op_1"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    target_length=500.0), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_6_entity["op_3"],
                    end=DirectionalCouplerBend_4_entity["op_0"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    target_length=500.0), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_6_entity["op_2"],
                    end=DirectionalCouplerBend_4_entity["op_1"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_5_entity["op_3"],
                    end=Fixed_Terminator_TE_1550_2_entity["op_0"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_5_entity["op_0"],
                    end=DirectionalCouplerBend_1_entity["op_3"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    target_length=300.0,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_3_entity["op_2"],
                    end=Fixed_Terminator_TE_1550_1_entity["op_0"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_3_entity["op_3"],
                    end=DirectionalCouplerBend_2_entity["op_2"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_3_entity["op_1"],
                    end=DirectionalCouplerBend_7_entity["op_2"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    target_length=300.0,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_3_entity["op_0"],
                    end=DirectionalCouplerBend_7_entity["op_3"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_1_entity["op_2"],
                    end=DirectionalCouplerBend_5_entity["op_1"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_2_entity["op_3"],
                    end=DirectionalCouplerBend_5_entity["op_2"],
                    waypoints=[fp.Offset.from_start(0,200)],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_1_entity["op_0"],
                    end=Fixed_Photo_Detector_4_entity["op_0"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_1_entity["op_1"],
                    end=Fixed_Photo_Detector_3_entity["op_0"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_7_entity["op_0"],
                    end=Fixed_Photo_Detector_2_entity["op_0"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
                fp.LinkBetween(
                    start=DirectionalCouplerBend_7_entity["op_1"],
                    end=Fixed_Photo_Detector_1_entity["op_0"],
                    link_type=TECH.WG.SWG.C.WIRE,
                    bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS), 
            ],
        )
        instance_naming_table[links[0]] = "U1002X"
        instance_naming_table[links[1]] = "U1001X"
        instance_naming_table[links[2]] = "U1005X"
        instance_naming_table[links[3]] = "U1006X"
        instance_naming_table[links[4]] = "U1003X"
        instance_naming_table[links[5]] = "U1004X"
        instance_naming_table[links[6]] = "2"
        instance_naming_table[links[7]] = "5"
        instance_naming_table[links[8]] = "7"
        instance_naming_table[links[9]] = "8"
        instance_naming_table[links[10]] = "9"
        instance_naming_table[links[11]] = "10"
        instance_naming_table[links[12]] = "11"
        instance_naming_table[links[13]] = "12"
        instance_naming_table[links[14]] = "13"
        instance_naming_table[links[15]] = "14"
        instance_naming_table[links[16]] = "15"
        instance_naming_table[links[17]] = "16"
        insts += links

        waylines=[
        ]
        insts += waylines

        return insts, elems, ports

if __name__ == "__main__":

    import gpdk.components.all
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    spc_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".spc").name
    library = fp.Library()

    TECH = get_technology()

    instance_naming_table: Dict[fp.ICellRef, str] = {}

    device = example_demultiplexer21()
    instance_naming_table.update(device.instance_naming_table)

    library += device


    fp.export_gds(library, file=gds_file)
    fp.export_spc(library, file=spc_file, components=gpdk.components.all)
    fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=gpdk.components.all, instance_naming_table=instance_naming_table)

