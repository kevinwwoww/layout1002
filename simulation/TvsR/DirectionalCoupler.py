from gpdk import all as pdk
from gpdk.technology import get_technology
from simulation import all as sim
TECH = get_technology()
# ========================================================================= #

# Call component
DC = pdk.DirectionalCouplerSBend(
    waveguide_type=TECH.WG.SWG.C.WIRE,
    bend_radius=20,
    coupler_length=4,
    coupler_spacing=5)
# generate .lsf file and run
sim.fdtd_run_Trans(
    device=DC,
    gdsfile_name="DC_SBend",
    op_in="op_0",
    core_layer="2:1",
    slab_silicon_thickness=0.08,
    wavelength_start=1.5,
    wavelength_stop=1.6,
    time=500,
    mesh_accuracy=2,
    freq_points=500,
    mode="TE"
)



