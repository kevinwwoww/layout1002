from gpdk import all as pdk
from gpdk.technology import get_technology
TECH = get_technology()
from simulation import all as sim
# ========================================================================= #
# Call component
splitter = pdk.YSplitter(
    waveguide_type=TECH.WG.FWG.C.WIRE
)

sim.fdtd_run_spar(
    device=splitter,
    gdsfile_name="y_splitter",
    wavelength_start=1.530,
    wavelength_stop=1.565,
    core_layer="1:1",
    time=1000,
    mesh_accuracy=2,
    freq_points=351,
    mode="TE"
)