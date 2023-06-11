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
    s = pdk.Straight(length=20, waveguide_type=TECH.WG.FWG.C.WIRE, port_names=["op_0", fp.Hidden("op_1")])
    library += s
    # custom region end

    # fixed template start
    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    print(fp.distance_between(s["op_0"].position, s["op_1"].position))
    # fp.plot(library)
    # fixed template end
