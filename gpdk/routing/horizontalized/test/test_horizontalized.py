from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)  # (plot_differences=True)
def test_horizontalized():
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    from gpdk.components.bend.bend_circular import BendCircular

    library += pdk.Horizontalized(device=BendCircular(radius=30, waveguide_type=TECH.WG.FWG.C.WIRE, transform=fp.rotate(degrees=30)))

    # fmt: on
    # =============================================================
    # fp.plot(library)
    return library
