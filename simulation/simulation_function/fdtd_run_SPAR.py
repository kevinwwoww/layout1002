import sys
from pathlib import Path
import math
from fnpcell import all as fp
from gpdk.technology import get_technology
TECH = get_technology()
from .fdtd_run_lsf import fdtd_run
from gpdk import all as pdk

def fdtd_run_spar(
        *,
        device: fp.DeviceParam(),
        gdsfile_name: str,
        gds_topcell: str = "Extended",
        z_size: float = 1,
        mesh_accuracy: int = 2,
        mode: str = "TE",
        time: int = 1000,
        freq_points: int = 1000,
        wavelength_start: float = 1.5,
        wavelength_stop: float = 1.6,
        Top_silicon_thickness: float = 0.22,
        BOX_sio2_thickness: float = 2,
        Cladding_sio2_thickness: float = 2,
        slab_silicon_thickness: float = 0,
        auto_symmetry: bool = True,
        core_layer: str = "1:1",
        hide: bool = False,
        exit: bool = True
):

    um = 1e-06
    fs = 1e-15
    if auto_symmetry is True:
        auto_symmetry = 1
    else:
        auto_symmetry = 0

    region = fp.get_bounding_box(device)
    n_ports = len(device.ports)

    instSet, elemSet, portSet = fp.InstanceSet(), fp.ElementSet(), fp.PortSet()
    instSet += pdk.Extended(device=device, lengths={"*": 0.5})
    extended = fp.Device(content=instSet + elemSet, ports=portSet)
    local = Path(sys.argv[0]).parent / "local" / f"{gdsfile_name}"
    gds_file = local / f"{gdsfile_name}.gds"
    
    library = fp.Library()
    library += extended
    fp.export_gds(library, file=gds_file)
    fp.plot(library)

    x_min = region[0][0]
    y_min = region[0][1]
    x_max = region[1][0]
    y_max = region[1][1]

    lsf = open(f"{local}\\{gdsfile_name}.lsf", 'w')
    lsf.write(f"cd('{local}');"'\n'
              "deleteall;"'\n'
              "addfdtd;"'\n'
              "set('dimension', '3D');"'\n'
              f"set('x min', {x_min*um});"'\n'
              f"set('x max', {x_max*um});"'\n'
              f"set('y min', {y_min*um});"'\n'
              f"set('y max', {y_max*um});"'\n'
              f"set('z span', {z_size*um});"'\n'
              f"set('mesh accuracy', {mesh_accuracy});"'\n'
              f"set('simulation time', {time*fs});"'\n'
              )
    lsf.close()
    for i in range(n_ports):
        x = device[f"op_{i}"].position[0]*um
        y = device[f"op_{i}"].position[1]*um
        lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
        lsf.write("addport;"'\n'
                  f"set('name', 'op_{i}');"'\n'
                  f"set('x', {x});"'\n'
                  f"set('y', {y});"'\n'
                  f"set('z span', {z_size*um});"'\n'
                  f"set('mode selection', 'fundamental {mode} mode');"'\n'
                  )
        lsf.close()
        if device[f"op_{i}"].orientation == 0:
            lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
            lsf.write("set('injection axis', 'x-axis');"'\n'
                      "set('direction', 'Backward');"'\n'
                      f"set('y span', {TECH.WG.FWG.C.WIRE.core_width*3*um});"'\n'
                      )
            lsf.close()
        if device[f"op_{i}"].orientation == math.pi/2:
            lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
            lsf.write("set('injection axis', 'y-axis');"'\n'
                      "set('direction', 'Backward');"'\n'
                      f"set('x span', {TECH.WG.FWG.C.WIRE.core_width*3*um});"'\n'
                      )
            lsf.close()
        if device[f"op_{i}"].orientation == math.pi:
            lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
            lsf.write("set('injection axis', 'x-axis');"'\n'
                      "set('direction', 'Forward');"'\n'
                      f"set('y span', {TECH.WG.FWG.C.WIRE.core_width*3*um});"'\n'
                      )
            lsf.close()
        if device[f"op_{i}"].orientation == -math.pi/2:
            lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
            lsf.write("set('injection axis', 'y-axis');"'\n'
                      "set('direction', 'Forward');"'\n'
                      f"set('x span', {TECH.WG.FWG.C.WIRE.core_width*3*um});"'\n'
                      )
            lsf.close()
    lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
    lsf.write(f"setnamed('FDTD::ports', 'monitor frequency points', {freq_points});"'\n'
              f"setglobalsource('wavelength start', {wavelength_start*um});"'\n'
              f"setglobalsource('wavelength stop', {wavelength_stop*um});"'\n'
              )
    lsf.close()

    lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
    lsf.write("addrect;"'\n'
              "set('name', 'BOX');"'\n'
              f"set('x min', {(x_min - 0.5)*um});"'\n'
              f"set('x max', {(x_max + 0.5)*um});"'\n'
              f"set('y min', {(y_min - 0.5)*um});"'\n'
              f"set('y max', {(y_max + 0.5)*um});"'\n'
              f"set('alpha', 0.5);"'\n'
              f"set('z min', {-Top_silicon_thickness*um/2 - BOX_sio2_thickness*um});"'\n'
              f"set('z max', {-Top_silicon_thickness*um/2});"'\n'
              f"set('material', 'SiO2 (Glass) - Palik');"'\n'
              )
    lsf.close()

    lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
    lsf.write("addrect;"'\n'
              "set('name', 'CLADD');"'\n'
              f"set('x min', {(x_min - 0.5)*um});"'\n'
              f"set('x max', {(x_max + 0.5)*um});"'\n'
              f"set('y min', {(y_min - 0.5)*um});"'\n'
              f"set('y max', {(y_max + 0.5)*um});"'\n'
              f"set('alpha', 0.5);"'\n'
              f"set('z min', {-Top_silicon_thickness*um/2});"'\n'
              f"set('z max', {-Top_silicon_thickness*um/2 + Cladding_sio2_thickness*um});"'\n'
              f"set('material', 'SiO2 (Glass) - Palik');"'\n'
              )
    lsf.close()

    lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
    lsf.write("addrect;"'\n'
              "set('name', 'slab');"'\n'
              f"set('x min', {(x_min - 0.5) * um});"'\n'
              f"set('x max', {(x_max + 0.5) * um});"'\n'
              f"set('y min', {(y_min - 0.5) * um});"'\n'
              f"set('y max', {(y_max + 0.5) * um});"'\n'
              f"set('z min', {-Top_silicon_thickness*um/2});"'\n'
              f"set('z max', {-Top_silicon_thickness*um/2 + slab_silicon_thickness*um});"'\n'
              f"set('material', 'Si (Silicon) - Palik');"'\n'
              )
    lsf.close()

    lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
    lsf.write(f"gdsimport('{gdsfile_name}.gds', '{gds_topcell}', '{core_layer}');"'\n'
              f"set('z span', {Top_silicon_thickness*um});"'\n'
              f"set('material', 'Si (Silicon) - Palik');"'\n'
              )
    lsf.close()

    lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
    lsf.write(f"save('{gdsfile_name}.fsp');"'\n')
    lsf.close()

    lsf = open(f"{local}\\{gdsfile_name}.lsf", 'a')
    lsf.write("addsweep(3);"'\n'
              "setsweep('s-parameter sweep', 'Excite all ports', 0);"'\n'
              f"setsweep('s-parameter sweep', 'auto symmetry', {auto_symmetry});"'\n'
              "runsweep('s-parameter sweep');"'\n'
              f"exportsweep('s-parameter sweep', '{gdsfile_name}.dat');"
              )
    lsf.close()
    fdtd_run(lsf_path=f"{local}\\{gdsfile_name}.lsf", hide=hide, exit=exit)

