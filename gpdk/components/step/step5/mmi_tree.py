from dataclasses import dataclass
from typing import Mapping, cast

from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.components.step.step2.mmi1x2 import MMI1x2


@dataclass(eq=False)
class MMITree(fp.PCell):
    x_spacing: float = fp.PositiveFloatParam(default=50)
    end_y_spacing: float = fp.PositiveFloatParam(default=50)
    order: float = fp.PositiveFloatParam(default=5)
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        x_spacing = self.x_spacing
        end_y_spacing = self.end_y_spacing
        order = self.order
        mmi = MMI1x2()
        num_per_col = []
        v_spacing = []

        for i in range(order):
            num_per_col.append(2**i)
            v_spacing.append(end_y_spacing*(2**(order - i - 1)))

        for i in range(order):
            for j in range(num_per_col[i]):
                x = i * x_spacing
                y = (-(num_per_col[i] - 1) * v_spacing[i]/2) + j * v_spacing[i] # bottom mmi y = 0
                mmi = mmi["op_0"].repositioned(at=(x,y)).owner
                insts += mmi, f"{i},{j}"

        mmi_tree = cast(Mapping[str, fp.ICellRef], insts)
        for i in range(order):
            for j in range(num_per_col[i]):
                if i < order-1:
                    link1 = fp.LinkBetween(start=mmi_tree[f"{i},{j}"]["op_1"],
                                           end=mmi_tree[f"{i+1},{2*j}"]["op_0"],
                                           bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR)
                    insts += link1
                    link2 = fp.LinkBetween(start=mmi_tree[f"{i},{j}"]["op_2"],
                                           end=mmi_tree[f"{i+1},{2*j+1}"]["op_0"],
                                           bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR)
                    insts += link2

        ports += mmi_tree["0,0"]["op_0"].with_name("op_0")
        for i in range(num_per_col[-1]):
            # put ports on the last column of the tree
            ports += mmi_tree[f"{order - 1},{i}"]["op_1"].with_name(f"op_{2*i+1}")
            ports += mmi_tree[f"{order - 1},{i}"]["op_2"].with_name(f"op_{2*i+2}")

        # print(v_spacing)
        print(mmi_tree["4,1"]["op_0"].position)

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".gds").name
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += MMITree()
    device = MMITree()
    cor = device.polygon_set(layer=TECH.LAYER.FWG_COR)
    cld = device.polygon_set(layer=TECH.LAYER.FWG_CLD)
    tre = fp.el.PolygonSet.boolean_sub(cld, cor, layer=TECH.LAYER.FWG_TRE)
    library += fp.Device(content=[tre.translated(300, 0)], ports=[])

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
    print(MMITree())
