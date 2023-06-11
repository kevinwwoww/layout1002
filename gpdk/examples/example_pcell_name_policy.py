from dataclasses import dataclass
from typing import Tuple
from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class WithDefaultNamePrefix(fp.PCell):
    size: float = fp.FloatParam()

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        elems += fp.el.Rect(center=(0, 0), width=self.size, height=self.size, layer=TECH.LAYER.M1_DRW)
        return insts, elems, ports


@dataclass(eq=False)
class WithBlankNamePrefix(fp.PCell):
    name: str = fp.NameParam(prefix="")
    size: float = fp.FloatParam()

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        elems += fp.el.Rect(center=(0, 0), width=self.size, height=self.size, layer=TECH.LAYER.M2_DRW)
        return insts, elems, ports


@dataclass(eq=False)
class WithCustomNamePrefix(fp.PCell):
    name: str = fp.NameParam(prefix="custom")
    size: float = fp.FloatParam()

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        elems += fp.el.Rect(center=(0, 0), width=self.size, height=self.size, layer=TECH.LAYER.MT_DRW)
        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file
    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================

    # all cell names are possibly with a suffix to avoid name collision

    # gds cell name: WithDefaultNamePrefix, using class name as prefix
    # library += WithDefaultNamePrefix(size=10)
    # gds cell name: WithDefaultNamePrefix_N1, using class name as prefix
    # library += WithDefaultNamePrefix(name="N1", size=20)
    # gds cell name: N1, force to use "N1" as cell name
    # library += WithDefaultNamePrefix(size=30, name="N2").with_name("N1")

    # # gds cell name: WithBlankNamePrefix
    # library += WithBlankNamePrefix(size=40)
    # gds cell name: N1, no prefix
    # library += WithBlankNamePrefix(name="N1", size=50)
    # # gds cell name: N1, force to use "N1" as cell name
    # library += WithBlankNamePrefix(size=60, name="N2").with_name("N1")
    #
    # # gds cell name: custom
    library += WithCustomNamePrefix(size=70)
    # # gds cell name: custom_N1
    library += WithCustomNamePrefix(name="N1", size=80)
    # # gds cell name: N1
    library += WithCustomNamePrefix(size=90, name="N1").with_name("N2")

    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
