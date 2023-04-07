from fnpcell import all as fp
from collections import OrderedDict
import numpy as np
from api_load import simulation
from gpdk.technology import get_technology
import math
TECH = get_technology()
def SimFDTD(
        *,
        device: fp.DeviceParam(),
        file_name: str,
        cell_name: str = "Extended",
        z_size: float = 1,
        mesh_accuracy: int = 2,
        n_modes: list = None,
        time: int = 1000,
        wavelength_start: float = 1.5,
        wavelength_stop: float = 1.6,
        Top_silicon_thickness: float = 0.22,
        BOX_sio2_thickness: float = 2,
        Cladding_sio2_thickness: float = 2,
        slab_silicon_thickness: float = 0,
        hide: bool = False,
        auto_symmetry: bool = False,
        group_delay: bool = True
):
    # ================ set properties ================ #
    if n_modes is None:
        n_modes = [1]
    um = 1e-06
    fs = 1e-15
    n_mode = np.array(n_modes)
    region = fp.get_bounding_box(device)

    x_min = region[0][0]
    y_min = region[0][1]
    x_max = region[1][0]
    y_max = region[1][1]
# ============================== build simulation region ========================= #
    fdtd = simulation(hide=hide)
    fdtd_props = OrderedDict(
        [("dimension", "3D"), ("x min", x_min*um), ("x max", x_max*um),
         ("z span", z_size*um), ("y min", y_min*um), ("y max", y_max*um),
         ("mesh accuracy", mesh_accuracy), ("simulation time", time*fs)])
    fdtd.addfdtd(properties=fdtd_props)

    profile_props = OrderedDict(
        [("name", "profile"), ("x min", x_min*um), ("x max", x_max*um),
         ("y min", y_min*um), ("y max", y_max*um),
         ("override global monitor settings", True), ("frequency points", 11.0)])
    fdtd.addprofile(properties=profile_props)

    fdtd.setglobalsource("wavelength start", wavelength_start*um)
    fdtd.setglobalsource("wavelength stop", wavelength_stop*um)

    n_ports = len(device.ports)
    rad2deg = 180/math.pi
    for i in range(n_ports):
        fdtd.addport()
        fdtd.set("name", f"op_{i}")
        fdtd.set("x", device[f"op_{i}"].position[0]*um)
        fdtd.set("y", device[f"op_{i}"].position[1]*um)
        fdtd.set("z span", z_size*um)
        fdtd.set("mode selection", "user select")
        fdtd.set("selected mode numbers", n_mode)
        if device[f"op_{i}"].orientation == 0:
            fdtd.set("injection axis", "x-axis")
            fdtd.set("direction", "Backward")
            fdtd.set("y span", TECH.WG.FWG.C.WIRE.core_width*2*um)
        if device[f"op_{i}"].orientation == math.pi/2:
            fdtd.set("injection axis", "y-axis")
            fdtd.set("direction", "Backward")
            fdtd.set("x span", TECH.WG.FWG.C.WIRE.core_width*2*um)
        if device[f"op_{i}"].orientation == math.pi:
            fdtd.set("injection axis", "x-axis")
            fdtd.set("direction", "Forward")
            fdtd.set("y span", TECH.WG.FWG.C.WIRE.core_width*2*um)
        if device[f"op_{i}"].orientation == -math.pi/2:
            fdtd.set("injection axis", "y-axis")
            fdtd.set("direction", "Forward")
            fdtd.set("x span", TECH.WG.FWG.C.WIRE.core_width*2*um)
        if 0 < device[f"op_{i}"].orientation < math.pi/2:
            fdtd.set("injection axis", "x-axis")
            fdtd.set("direction", "Backward")
            fdtd.set("y span", TECH.WG.FWG.C.WIRE.core_width*2*um)
            fdtd.set("theta", device[f"op_{i}"].orientation*rad2deg)
        if math.pi/2 < device[f"op_{i}"].orientation < math.pi:
            fdtd.set("injection axis", "x-axis")
            fdtd.set("direction", "Forward")
            fdtd.set("y span", TECH.WG.FWG.C.WIRE.core_width*2*um)
            fdtd.set("theta", device[f"op_{i}"].orientation*rad2deg-180)
        if -math.pi/2 < device[f"op_{i}"].orientation < 0:
            fdtd.set("injection axis", "x-axis")
            fdtd.set("direction", "Backward")
            fdtd.set("y span", TECH.WG.FWG.C.WIRE.core_width*2*um)
            fdtd.set("theta", device[f"op_{i}"].orientation*rad2deg)
        if -math.pi < device[f"op_{i}"].orientation < -math.pi/2:
            fdtd.set("injection axis", "x-axis")
            fdtd.set("direction", "Forward")
            fdtd.set("y span", TECH.WG.FWG.C.WIRE.core_width*2*um)
            fdtd.set("theta", 180+device[f"op_{i}"].orientation*rad2deg)


    fdtd.setnamed("FDTD::ports", "monitor frequency points", 1000)
    fdtd.setnamed("FDTD::ports", "Calculate group delay", 1)
# =========================== build structures ======================== #
    BOX_props = OrderedDict(
        [("name", "BOX"), ("x min", (x_min - 0.5)*um), ("x max", (x_max + 0.5)*um),
         ("y min", (y_min - 0.5)*um), ("y max", (y_max + 0.5)*um), ("alpha", 0.5),
         ("z min", -Top_silicon_thickness*um/2 - BOX_sio2_thickness*um), ("z max", -Top_silicon_thickness*um/2),
         ("material", "SiO2 (Glass) - Palik")])
    fdtd.addrect(properties=BOX_props)

    CLD_props = OrderedDict(
        [("name", "CLD"), ("x min", (x_min - 0.5)*um), ("x max", (x_max + 0.5)*um),
         ("y min", (y_min - 0.5)*um), ("y max", (y_max + 0.5)*um), ("alpha", 0.5),
         ("z max", -Top_silicon_thickness*um/2 + Cladding_sio2_thickness*um), ("z min", -Top_silicon_thickness*um/2),
         ("material", "SiO2 (Glass) - Palik")])
    fdtd.addrect(properties=CLD_props)

    slab_props = OrderedDict(
        [("name", "slab"), ("x min", (x_min - 0.5) * um), ("x max", (x_max + 0.5) * um),
         ("y min", (y_min - 0.5) * um), ("y max", (y_max + 0.5) * um),
         ("z min", -Top_silicon_thickness*um/2),
         ("z max", -Top_silicon_thickness*um/2 + slab_silicon_thickness*um),
         ("material", "Si (Silicon) - Palik")])
    fdtd.addrect(properties=slab_props)

    fdtd.gdsimport(f"local\\{file_name}.gds", f"{cell_name}", "1:1")
    fdtd.set("z span", Top_silicon_thickness*um)
    fdtd.set("material", "Si (Silicon) - Palik")

    fdtd.save(f"local\\{file_name}.fsp")

    fdtd.addsweep(3)
    # un-check "Excite all ports" option
    fdtd.setsweep("s-parameter sweep", "Excite all ports", 0)
    # use auto-symmetry to populate the S-matrix setup table
    fdtd.setsweep("s-parameter sweep", "auto symmetry", auto_symmetry)
    fdtd.setsweep("s-parameter sweep", "Calculate group delay", group_delay)
    if group_delay is True:
        fdtd.setsweep("s-parameter sweep", "Include group delay", 1)
    else:
        fdtd.setsweep("s-parameter sweep", "Include group delay", 0)
    # run s-parameter sweep
    fdtd.runsweep("s-parameter sweep")
    # collect results
    fdtd.exportsweep("s-parameter sweep", f"{file_name}.dat")


