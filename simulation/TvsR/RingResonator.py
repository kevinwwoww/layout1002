from gpdk import all as pdk
from gpdk.technology import get_technology
from simulation import all as sim
TECH = get_technology()
# ========================================================================= #

# Call component
RingResonator = pdk.RingResonator(
    ring_type=TECH.WG.FWG.C.WIRE,
    ring_radius=20
)
sim.fdtd_run_Trans(
    device=RingResonator,
    gdsfile_name="ring_resonator",
    op_in="op_0",
    slab_silicon_thickness=0.08,
    wavelength_start=1.5,
    wavelength_stop=1.6,
    time=500,
    mesh_accuracy=1,
    freq_points=500,
    mode="TE"
)
