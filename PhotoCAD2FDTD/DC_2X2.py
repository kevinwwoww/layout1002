from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from os import path
from sim_s import Sim_S
TECH = get_technology()
# ========================================================================= #
# Call component
DC = pdk.DirectionalCouplerSBend(waveguide_type=TECH.WG.FWG.C.WIRE.updated(core_design_width=0.45), coupler_spacing=0.65, bend_radius=5, straight_after_bend=3)
# Port extension
device = pdk.Extended(device=DC, lengths={"*": 1})
# Define the path of the .gds file
gds_file = path.join(path.dirname(__file__), "local", "DC_2X2.gds")
# GDS export
fp.export_gds(device, file=gds_file)
fp.plot(device)
# S-Parameters Export
Sim_S(device=DC, file_name="DC_2X2", time=30000, n_modes=[1], auto_symmetry=True)
