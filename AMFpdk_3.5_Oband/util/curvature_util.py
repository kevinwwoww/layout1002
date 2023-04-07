# type: ignore
from typing import Iterable, Optional, Union

import numpy as np
import matplotlib.pyplot as plt
from fnpcell import all as fp
from numpy import ndarray


def plot_curvature(curve: fp.ICurve):

    points = curve.curve_points
    t = np.array(range(len(points)))
    shape = np.array(points)

    # fi, (ax1, ax2, ax3) = plt.subplots(ncols=3, nrows=1)
    fi, (ax1, ax3) = plt.subplots(ncols=2, nrows=1)

    ax1.plot(shape[:, 0], shape[:, 1])
    ax1.set_ylabel("y")
    ax1.set_xlabel("x")
    # ax1.axis("eaual")

    # ax2.plot(t, 1 / abs(kappa))
    # ax2.set_ylabel("bend_radius")
    # ax2.set_xlabel("t")
    # # #ax2.axis("raduis")

    kappa = fp.curvature_of(shape)
    ax3.plot(t[5:-5], np.round(np.abs(kappa[5:-5]), 6))
    ax3.set_ylabel("Curvature")
    ax3.set_xlabel("t")
    # ax3.tight_layout()

    plt.show(block=True)


if __name__ == "__main__":
    from AMFpdk.technology import get_technology
    import warnings

    warnings.simplefilter("error")
    TECH = get_technology()

    curve = fp.g.EulerBend(p=0, degrees=180, radius_min=1, angle_step=0.01)
    plot_curvature(curve)

    curve = fp.g.EulerBend(p=1, degrees=180, radius_min=1, angle_step=0.01)
    plot_curvature(curve)

    curve = fp.g.EulerBend(p=0.2, degrees=180, radius_min=1, angle_step=0.01)
    plot_curvature(curve)

    curve = fp.g.CosineBend(p=0, degrees=180, radius_min=1, angle_step=0.01)
    plot_curvature(curve)

    curve = fp.g.CosineBend(p=1, degrees=180, radius_min=1, angle_step=0.01)
    plot_curvature(curve)

    curve = fp.g.CosineBend(p=0.2, degrees=180, radius_min=1, angle_step=0.01)
    plot_curvature(curve)
