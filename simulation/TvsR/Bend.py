from gpdk import all as pdk
from gpdk.technology import get_technology
import simulation as sim
TECH = get_technology()

# ========================================================================= #

# Call component
EBend = pdk.BendEuler90(waveguide_type=TECH.WG.MWG.C.WIRE, radius_eff=10)
# generate .lsf file and run
sim.fdtd_run_Trans(
    device=EBend,
    gdsfile_name="Euler_Bend",
    op_in="op_0",
    wavelength_start=1.548,
    wavelength_stop=1.552,
    core_layer="3:1",
    slab_silicon_thickness=0.07,
    time=1000,
    mesh_accuracy=2,
    freq_points=500,
    mode="TE"
)



