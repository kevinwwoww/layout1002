from dataclasses import dataclass
from typing import Mapping, cast

from fnpcell import all as fp

# from crosswaveguide import Crosswg
from AMFcrosswaveguide import Cwg as Crosswg
# from step2.mmi1x2 import MMI1x2

from AMFpdk.components.mmi.mmi import MMI1x2

from AMFpdk import all as pdk
from AMFpdk.technology import get_technology
from AMFpdk.technology.waveguide_factory import StraightFactory
from AMFpdk.technology.waveguide_factory import EulerBendFactory
from AMFpdk.components.straight.straight import Straight as RingModulator
# from AMFpdk.components.ring_resonator.ring_resonator import RingResonator as RingModulator

# def bend_factories(waveguide_type: fp.IWaveguideType):
#     if waveguide_type == TECH.WG.FWG.C.WIRE:
#         return EulerBendFactory(radius_min=6, l_max=5, waveguide_type=waveguide_type)
#     return waveguide_type.bend_factory

def sp_num(order):
    spnum=0
    for i in range(order):
        spnum = spnum+2**i
    return spnum

def isPower(row_number):
    mmi_tree_order = 0
    while(1):
        if row_number % 2==0:
            mmi_tree_order = mmi_tree_order+1
            row_number =row_number/2
        else:
            return mmi_tree_order


@dataclass(eq=False)
class TICircuit(fp.PCell):
    def build(self):
        global spacing, row_number
        insts, elems, ports = super().build()
        TECH = get_technology()

        spacing = 200
        ##row_number必须为4*(2**n)
        row_number = 64

        basic_comp = RingModulator()
        basic_comp_y = RingModulator(transform=fp.rotate(degrees=90))

        mmi_tree_order = isPower(row_number/4)
        mmi_tree_sp = sp_num(mmi_tree_order)
        # print(mmi_tree_order,mmi_tree_sp)

        mmi_number_height = []
        cwg1_number_height = []
        cwg2_number_height = []
        cwg3_number_height = []

        for i in range(mmi_tree_order+1,1,-1):
            mmi_number_height.append((mmi_tree_order+1)*(i))
            cwg1_number_height.append(mmi_number_height[mmi_tree_order+1-i]-0.5)
            cwg2_number_height.append(mmi_number_height[mmi_tree_order+1-i]-1)
            cwg3_number_height.append(mmi_number_height[mmi_tree_order+1-i]-1.5)

        mmi = MMI1x2(transform=fp.rotate(degrees=270))
        cwg = Crosswg()

        yy_spacing = []

        for i in range(row_number):
            yy_spacing.append(spacing * (i + 0.5))

        for i in range(row_number):
            y = spacing
            x = yy_spacing[i]
            y_module = basic_comp_y["op_0"].repositioned(at=(x, y)).owner
            insts += y_module, f"{0},{0},{0},{i}"


        for i in range(mmi_tree_order):
            for j in range (2**i):
                mmi_tree_num = 0
                for k in range(int(row_number*((1/2)**(i+1)))+(j)*(2**(mmi_tree_order+2-i))-2,(int(row_number*((1/2)**(i+1)))+(j)*(2**(mmi_tree_order+2-i))+2)):
                    y = spacing*mmi_number_height[i]
                    x = yy_spacing[k]
                    mmi_tree = mmi["op_0"].repositioned(at=(x,y)).owner
                    insts += mmi_tree, f"{1},{i},{j},{mmi_tree_num}"
                    mmi_tree_num = mmi_tree_num+1
                cwg1_tree_number = 0
                cwg2_tree_number = 0
                cwg3_tree_number = 0
                for k in range(int(row_number*((1/2)**(i+1)))+(j)*(2**(mmi_tree_order+2-i))-2,(int(row_number*((1/2)**(i+1)))+(j)*(2**(mmi_tree_order+2-i))+1)):
                    y = spacing*cwg1_number_height[i]
                    x = yy_spacing[k]+0.5*spacing
                    cwg_tree = cwg["op_0"].repositioned(at=(x,y)).owner
                    insts += cwg_tree, f"{2},{i},{j},{cwg1_tree_number}"
                    cwg1_tree_number = cwg1_tree_number+1
                for k in range(int(row_number*((1/2)**(i+1)))+(j)*(2**(mmi_tree_order+2-i))-1,(int(row_number*((1/2)**(i+1)))+(j)*(2**(mmi_tree_order+2-i))+1)):
                    y = spacing*cwg2_number_height[i]
                    x = yy_spacing[k]
                    cwg_tree = cwg["op_0"].repositioned(at=(x,y)).owner
                    insts += cwg_tree, f"{3},{i},{j},{cwg2_tree_number}"
                    cwg2_tree_number = cwg2_tree_number+1
                for k in range(int(row_number*((1/2)**(i+1)))+(j)*(2**(mmi_tree_order+2-i))-1,(int(row_number*((1/2)**(i+1)))+(j)*(2**(mmi_tree_order+2-i)))):
                    y = spacing*cwg3_number_height[i]
                    x = yy_spacing[k]+0.5*spacing
                    cwg_tree = cwg["op_0"].repositioned(at=(x,y)).owner
                    insts += cwg_tree, f"{4},{i},{j},{cwg3_tree_number}"
                    cwg3_tree_number = cwg3_tree_number+1

        progcuit = cast(Mapping[str, fp.ICellRef], insts)

        for i in range(mmi_tree_order):
            for j in range (2**i):
                if (i+1) < mmi_tree_order:
                    link100 = fp.LinkBetween(start=progcuit[f"{1},{i},{j},{0}"]["op_1"],
                                           end=progcuit[f"{1},{i+1},{2*j},{0}"]["op_0"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link100
                else:
                    link101 = fp.LinkBetween(start=progcuit[f"{1},{i},{j},{0}"]["op_1"],
                                           end=progcuit[f"{0},{0},{0},{j*8}"]["op_1"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link101
                link111 = fp.LinkBetween(start=progcuit[f"{1},{i},{j},{0}"]["op_2"],
                                       end=progcuit[f"{2},{i},{j},{0}"]["op_3"],
                                       bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link111
                link112 = fp.LinkBetween(start=progcuit[f"{2},{i},{j},{0}"]["op_1"],
                                         end=progcuit[f"{3},{i},{j},{0}"]["op_3"],
                                         bend_factory=EulerBendFactory(radius_min=5, l_max=5,
                                                                       waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link112
                link113 = fp.LinkBetween(start=progcuit[f"{3},{i},{j},{0}"]["op_1"],
                                         end=progcuit[f"{4},{i},{j},{0}"]["op_3"],
                                         bend_factory=EulerBendFactory(radius_min=5, l_max=5,
                                                                       waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link113
                if (i + 1) < mmi_tree_order:
                    link114 = fp.LinkBetween(start=progcuit[f"{4},{i},{j},{0}"]["op_1"],
                                             end=progcuit[f"{1},{i+1},{2*j+1},{0}"]["op_0"],
                                             bend_factory=EulerBendFactory(radius_min=5, l_max=5,
                                                                           waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link114
                else:
                    link115 = fp.LinkBetween(start=progcuit[f"{4},{i},{j},{0}"]["op_1"],
                                             end=progcuit[f"{0},{0},{0},{j*8+4}"]["op_1"],
                                             bend_factory=EulerBendFactory(radius_min=5, l_max=5,
                                                                           waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link115
                link201 = fp.LinkBetween(start=progcuit[f"{1},{i},{j},{1}"]["op_1"],
                                       end=progcuit[f"{2},{i},{j},{0}"]["op_2"],
                                       bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link201
                if (i+1) < mmi_tree_order:
                    link202 = fp.LinkBetween(start=progcuit[f"{2},{i},{j},{0}"]["op_0"],
                                           end=progcuit[f"{1},{i+1},{2*j},{1}"]["op_0"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link202
                else:
                    link203 = fp.LinkBetween(start=progcuit[f"{2},{i},{j},{0}"]["op_0"],
                                           end=progcuit[f"{0},{0},{0},{8*j+1}"]["op_1"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link203
                link211 = fp.LinkBetween(start=progcuit[f"{1},{i},{j},{1}"]["op_2"],
                                       end=progcuit[f"{2},{i},{j},{1}"]["op_3"],
                                       bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link211
                link212 = fp.LinkBetween(start=progcuit[f"{2},{i},{j},{1}"]["op_1"],
                                       end=progcuit[f"{3},{i},{j},{1}"]["op_3"],
                                       bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link212
                if (i+1) < mmi_tree_order:
                    link213 = fp.LinkBetween(start=progcuit[f"{3},{i},{j},{1}"]["op_1"],
                                           end=progcuit[f"{1},{i+1},{2*j+1},{1}"]["op_0"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link213
                else:
                    link214 = fp.LinkBetween(start=progcuit[f"{3},{i},{j},{1}"]["op_1"],
                                           end=progcuit[f"{0},{0},{0},{8*j+1+4}"]["op_1"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link214
                link301 = fp.LinkBetween(start=progcuit[f"{1},{i},{j},{2}"]["op_1"],
                                       end=progcuit[f"{2},{i},{j},{1}"]["op_2"],
                                       bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link301
                link302 = fp.LinkBetween(start=progcuit[f"{2},{i},{j},{1}"]["op_0"],
                                       end=progcuit[f"{3},{i},{j},{0}"]["op_2"],
                                       bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link302
                if (i+1) < mmi_tree_order:
                    link303 = fp.LinkBetween(start=progcuit[f"{3},{i},{j},{0}"]["op_0"],
                                           end=progcuit[f"{1},{i+1},{2*j},{2}"]["op_0"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link303
                else:
                    link304 = fp.LinkBetween(start=progcuit[f"{3},{i},{j},{0}"]["op_0"],
                                           end=progcuit[f"{0},{0},{0},{8*j+2}"]["op_1"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link304
                link311 = fp.LinkBetween(start=progcuit[f"{1},{i},{j},{2}"]["op_2"],
                                       end=progcuit[f"{2},{i},{j},{2}"]["op_3"],
                                       bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link311
                if (i+1) < mmi_tree_order:
                    link312 = fp.LinkBetween(start=progcuit[f"{2},{i},{j},{2}"]["op_1"],
                                           end=progcuit[f"{1},{i+1},{2*j+1},{2}"]["op_0"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link312
                else:
                    link313 = fp.LinkBetween(start=progcuit[f"{2},{i},{j},{2}"]["op_1"],
                                           end=progcuit[f"{0},{0},{0},{8*j+2+4}"]["op_1"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link313
                if (i+1) < mmi_tree_order:
                    link411 = fp.LinkBetween(start=progcuit[f"{1},{i},{j},{3}"]["op_2"],
                                           end=progcuit[f"{1},{i+1},{2*j+1},{3}"]["op_0"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link411
                else:
                    link412 = fp.LinkBetween(start=progcuit[f"{1},{i},{j},{3}"]["op_2"],
                                           end=progcuit[f"{0},{0},{0},{8*j+4+3}"]["op_1"],
                                           bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link412
                link401 = fp.LinkBetween(start=progcuit[f"{1},{i},{j},{3}"]["op_1"],
                                       end=progcuit[f"{2},{i},{j},{2}"]["op_2"],
                                       bend_factory=EulerBendFactory(radius_min=5, l_max=5, waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link401
                link402 = fp.LinkBetween(start=progcuit[f"{2},{i},{j},{2}"]["op_0"],
                                         end=progcuit[f"{3},{i},{j},{1}"]["op_2"],
                                         bend_factory=EulerBendFactory(radius_min=5, l_max=5,
                                                                       waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link402
                link403 = fp.LinkBetween(start=progcuit[f"{3},{i},{j},{1}"]["op_0"],
                                         end=progcuit[f"{4},{i},{j},{0}"]["op_2"],
                                         bend_factory=EulerBendFactory(radius_min=5, l_max=5,
                                                                       waveguide_type=TECH.WG.RIB.C.WIRE))
                insts += link403
                if (i + 1) < mmi_tree_order:
                    link404 = fp.LinkBetween(start=progcuit[f"{4},{i},{j},{0}"]["op_0"],
                                             end=progcuit[f"{1},{i+1},{2*j},{3}"]["op_0"],
                                             bend_factory=EulerBendFactory(radius_min=5, l_max=5,
                                                                           waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link404
                else:
                    link405 = fp.LinkBetween(start=progcuit[f"{4},{i},{j},{0}"]["op_0"],
                                             end=progcuit[f"{0},{0},{0},{j*8+3}"]["op_1"],
                                             bend_factory=EulerBendFactory(radius_min=5, l_max=5,
                                                                           waveguide_type=TECH.WG.RIB.C.WIRE))
                    insts += link405

        # fmt: on
        return insts, elems, ports


if __name__ == "__main__":
    from pathlib import Path

    gds_file = Path(__file__).parent / "GDS_Output" / Path(__file__).with_suffix(".gds").name

    library = fp.Library()
    row_number =0

    TECH = get_technology()
    # =============================================================
    # fmt: off

    library += [TICircuit()]

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.plot(library)
