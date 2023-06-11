from fnpcell import all as fp
from gpdk.components.fixed_photo_detector.fixed_photo_detector import Fixed_Photo_Detector
from gpdk.util.test_util import expect_same_content


@expect_same_content(plot_differences=True)
def test_fixed_photo_detector():
    library = fp.Library()

    # =======================================================================
    # fmt: off

    library += Fixed_Photo_Detector()

    # fmt: on
    # =============================================================
    return library
