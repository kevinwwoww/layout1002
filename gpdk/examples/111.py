from dataclasses import dataclass
from typing import Dict, Mapping, cast
from fnpcell import all as fp

from gpdk.technology import get_technology
from gpdk import all as pdk_all

try:
    from gpdk import func_all as func_all
except:
    pass

@dataclass(eq=False)
class demo_mzi(fp.PCell):

    instance_naming_table: Mapping[fp.ICellRef, str] = fp.MappingParam(default_factory=dict, locked=True, compare=False)
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()
        instance_naming_table = cast(Dict[fp.ICellRef, str], self.instance_naming_table)

        YCombiner_1_temp = pdk_all.YCombiner(
            bend_radius=15.0,
            out_degrees=90.0,
            center_waveguide_length=2.0,
            taper_length=0.1,
            waveguide_type=TECH.WG.FWG.C.WIRE
        ).h_mirrored(x=0)

        YSplitter_1_temp = pdk_all.YSplitter(
            bend_radius=15.0,
            out_degrees=90.0,
            center_waveguide_length=2.0,
            taper_length=0.1,
            waveguide_type=TECH.WG.FWG.C.WIRE
        ).h_mirrored(x=0)



        YCombiner_1_entity = YCombiner_1_temp.translated(0, 0)
        YSplitter_1_entity = YSplitter_1_temp.translated(100, 20)

        instance_naming_table[YCombiner_1_entity] = "YCombiner_1"
        insts += YCombiner_1_entity
        instance_naming_table[YSplitter_1_entity] = "YSplitter_1"
        insts += YSplitter_1_entity

        links = fp.create_links(
            specs=[
                fp.LinkBetween(
                    start=YCombiner_1_entity["op_0"],
                    end=YSplitter_1_entity["op_2"],
                    bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS),
                fp.LinkBetween(
                    start=YCombiner_1_entity["op_1"],
                    end=YSplitter_1_entity["op_1"],
                    # waypoints=[fp.Offset.from_end(-30,50)],
                    bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR,
                    linking_policy=TECH.LINKING_POLICY.LESS_TRANS),
            ],
        )
        instance_naming_table[links[0]] = "2"
        instance_naming_table[links[1]] = "3"
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

    device = demo_mzi()
    instance_naming_table.update(device.instance_naming_table)

    library += device


    fp.export_gds(library, file=gds_file)
    # fp.export_spc(library, file=spc_file, components=gpdk.components.all)
    # fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=gpdk.components./all, instance_naming_table=instance_naming_table)
    fp.plot(library)