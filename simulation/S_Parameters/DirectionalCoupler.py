from gpdk import all as pdk
from gpdk.technology import get_technology
from simulation import all as sim
TECH = get_technology()
# ========================================================================= #

# Call component
DC = pdk.DirectionalCouplerSBend(waveguide_type=TECH.WG.SWG.C.WIRE, bend_radius=20, coupler_length=3, coupler_spacing=2)
# generate .lsf file and run
sim.fdtd_run_spar(device=DC, gdsfile_name="DC_SBend", core_layer="2:1", slab_silicon_thickness=0.08, auto_symmetry=True)



