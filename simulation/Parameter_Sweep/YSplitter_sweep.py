from gpdk import all as pdk
from gpdk.technology import get_technology
from simulation import all as sim
TECH = get_technology()

# ================================== sweep ======================================= #
for i in range(5):
    YS = pdk.YSplitter(waveguide_type=TECH.WG.SWG.C.WIRE, taper_length=5+i*2)
    sim.fdtd_run_Trans(i=i, device=YS, gdsfile_name="YSplitter", op_in="op_0", core_layer="2:1", slab_silicon_thickness=0.08, exit=True)
# ================================== analyze ======================================= #
sim.analyze_result(points=2, gdsfile_name="YSplitter", data_name="YSplitter_T_op_1")





