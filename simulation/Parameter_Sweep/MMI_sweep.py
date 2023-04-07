from gpdk import all as pdk
from gpdk.technology import get_technology
from simulation import all as sim
TECH = get_technology()

# ================================== sweep ======================================= #
for i in range(4):
    MMI = pdk.Mmi(waveguide_type=TECH.WG.FWG.C.WIRE, length=5+i*2)
    sim.fdtd_run_Trans(i=i, device=MMI, gdsfile_name="MMI", op_in="op_0", mode="TM", exit=True)
# ================================== analyze ======================================= #
sim.analyze_result(points=2, gdsfile_name="MMI", data_name="MMI_T_op_1")





