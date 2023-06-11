from dataclasses import dataclass
from typing import Any, Dict
from fnpcell import all as fp
from gpdk.technology import get_technology
from gpdk import all as pdk


@dataclass(eq=False)
class Circuit01_double_bus_ring_resonator(fp.PCell):
    instance_naming_table: Dict[Any, str] = fp.MappingParam(default_factory=dict, locked=True, compare=False)
    dist: float = 400

    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        instance_naming_table = self.instance_naming_table
        dist = self.dist
        gc = pdk.GratingCoupler(waveguide_type=TECH.WG.SWG.C.WIRE)
        dc = pdk.DirectionalCouplerSBend(waveguide_type=TECH.WG.SWG.C.WIRE, coupler_spacing=4, bend_degrees=60)
        dc_distance = fp.distance_between(dc["op_0"].position, dc["op_3"].position)

        gc_0 = gc.rotated(degrees=180)
        instance_naming_table[gc_0] = "gc_0"
        insts += gc_0

        gc_1 = gc.translated(dist, 0)
        instance_naming_table[gc_1] = "gc_1"
        insts += gc_1

        gc_2 = gc.rotated(degrees=180).translated(0, dist)
        instance_naming_table[gc_2] = "gc_2"
        insts += gc_2

        gc_3 = gc.translated(dist, dist)
        instance_naming_table[gc_3] = "gc_3"
        insts += gc_3

        dc_0 = fp.place(dc, "op_1", at=((dist - dc_distance) / 2, 0))
        instance_naming_table[dc_0] = "dc_0"
        insts += dc_0

        dc_1 = fp.place(dc, "op_0", at=((dist - dc_distance) / 2, dist))
        instance_naming_table[dc_1] = "dc_1"
        insts += dc_1

        links = fp.create_links(
            link_type=TECH.WG.SWG.C.WIRE,
            bend_factory=TECH.WG.SWG.C.WIRE.BEND_EULER,
            specs=[
                dc_1["op_0"] >> gc_2["op_0"],
                dc_1["op_3"] >> gc_3["op_0"],
                dc_0["op_1"] >> gc_0["op_0"],
                dc_0["op_2"] >> gc_1["op_0"],
                (dc_1["op_1"] >> dc_0["op_0"], 400),
                (dc_1["op_2"] >> dc_0["op_3"], 500),
            ],
        )
        instance_naming_table[links[0]] = "dc1_gc2"
        instance_naming_table[links[1]] = "dc1_gc3"
        instance_naming_table[links[2]] = "dc0_gc0"
        instance_naming_table[links[3]] = "dc0_gc1"
        instance_naming_table[links[4]] = "dc1_dc0_1_0"
        instance_naming_table[links[5]] = "dc1_dc0_2_3"
        insts += links

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    from gpdk.components import all as components

    instance_naming_table: Dict[fp.ICellRef, str] = {}

    device = Circuit01_double_bus_ring_resonator()
    instance_naming_table.update(device.instance_naming_table)
    library += device

    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.export_spc(library, file=gds_file.with_suffix(".spc"), components=components)
    fp.export_pls(library, file=gds_file.with_suffix(".pls"), components=components, instance_naming_table=instance_naming_table)
    #  fp.plot(library)
