from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology

if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off

    bend_euler = pdk.BendEuler(radius_min=50, degrees=-90, waveguide_type=TECH.WG.FWG.C.WIRE)

    device = fp.Device(name="svrf", content=[bend_euler], ports=[])
    library += device

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.util.generate_svrf(top_cell_name="svrf", gds_path=gds_file, file=gds_file.with_suffix(".svrf"))
