from dataclasses import dataclass

from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology



@dataclass(eq=False)
class MMITree(fp.PCell):
    def build(self):
        insts, elems, ports = super().build()
        TECH = get_technology()

        x_spacing = 50
        end_y_spacing = 50
        order = 5
        mmi = pdk.Mmi1x2()
        num_per_col = []
        v_spacing = []

        for i in range(order):
            num_per_col.append(2**i)
            v_spacing.append(end_y_spacing*(2**(order - i - 1)))

        for i in range(order):
            for j in range(num_per_col[i]):
                x = i * x_spacing
                y = (-(num_per_col[i] - 1) * v_spacing[i]/2) + j * v_spacing[i]
                mmi = mmi["op_0"].repositioned(at=(x,y)).owner
                insts += mmi, f"{i},{j}"

        mmi_array = insts
        for i in range(order):
            for j in range(num_per_col[i]):
                if i < order-1:
                    link1 = fp.LinkBetween(start=mmi_array[f"{i},{j}"]["op_1"],
                                           end=mmi_array[f"{i+1},{2*j}"]["op_0"],
                                           bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR)
                    insts += link1
                    link2 = fp.LinkBetween(start=mmi_array[f"{i},{j}"]["op_2"],
                                           end=mmi_array[f"{i+1},{2*j+1}"]["op_0"],
                                           bend_factory=TECH.WG.FWG.C.WIRE.BEND_CIRCULAR)
                    insts += link2

        ports += mmi_array["0,0"]["op_0"].with_name("op_0")
        for i in range(num_per_col[-1]):
            ports += mmi_array[f"{order - 1},{i}"]["op_1"].with_name(f"op_{2*i+1}")
            ports += mmi_array[f"{order - 1},{i}"]["op_2"].with_name(f"op_{2*i+2}")

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()
    # =============================================================
    # fmt: off
    mmitree = MMITree()
    library += mmitree

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
