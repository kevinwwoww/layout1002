from gpdk import all as pdk
from gpdk.technology import get_technology
TECH = get_technology()
from simulation import all as sim
# ========================================================================= #
# Call component
MMI = pdk.Mmi(
    waveguide_type=TECH.WG.FWG.C.WIRE,
    length=8,
    mid_wav_core_width=5,
    trace_spacing=1.5,
    wav_core_width=1.2,
    n_inputs=2
)

# generate .lsf file and run
sim.fdtd_run_spar(
    device=MMI,
    gdsfile_name="MMI2x2",
    wavelength_start=1.530,
    wavelength_stop=1.565,
    core_layer="1:1",
    time=1000,
    mesh_accuracy=2,
    freq_points=351,
    mode="TE"
)


