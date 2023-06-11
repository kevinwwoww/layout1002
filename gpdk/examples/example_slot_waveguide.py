from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology


if __name__ == "__main__":
    # fixed template start
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()

    # =============================================================
    # fmt: off
    # fixed template end

    # custom region start
    straight = pdk.Straight(length=20, waveguide_type=TECH.WG.SLOT.C.WIRE)

    library += straight
    # custom region end

    # fixed template start
    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
    # fixed template end
