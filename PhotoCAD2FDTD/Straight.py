from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from os import path
# from sim_s import Sim_S
TECH = get_technology()
# ========================================================================= #
# Call component
Straight = pdk.Straight(waveguide_type=TECH.WG.FWG.C.WIRE, length=10)
# Port extension
device = pdk.Extended(device=Straight, lengths={"*": 1})
# Define the path of the .gds file
gds_file = path.join(path.dirname(__file__), "local", "Straight.gds")
# GDS export
fp.export_gds(device, file=gds_file)
fp.plot(device)
# S-Parameters Export
Sim_S(device=Straight, file_name="Straight", time=30000, n_modes=[1])
