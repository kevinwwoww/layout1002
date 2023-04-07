from gpdk import all as pdk
from gpdk.technology import get_technology
from simulation import all as sim
TECH = get_technology()
# ========================================================================= #

# Call component
MMI = pdk.Mmi(
    waveguide_type=TECH.WG.FWG.C.WIRE,
    length=5,
    wav_core_width=1.2,
    transition_length=4
)

sim.analyze_result(points=2, data_name="MMI_T_op_", gdsfile_name="MMI")
# generate .lsf file and run
# sim.fdtd_run_Trans(
#     device=MMI,
#     gdsfile_name="MMI",
#     op_in="op_0",
#     mesh_accuracy=2,
#     freq_points=1000,
#     time=1000,
#     wavelength_start=1.548,
#     wavelength_stop=1.552,
# )
#
#

