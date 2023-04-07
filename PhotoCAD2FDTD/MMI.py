from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from os import path
from SimFDTD import SimFDTD
TECH = get_technology()
# ========================================================================= #
# Call component
MMI = pdk.Mmi(waveguide_type=TECH.WG.FWG.C.WIRE, n_inputs=2, n_outputs=2, length=5, transition_length=5, trace_spacing=2, mid_wav_core_width=4)
# Port extension
device = pdk.Extended(device=MMI, lengths={"*": 1})
# Define the path of the .gds file
gds_file = path.join(path.dirname(__file__), "local", "MMI.gds")
# GDS export
fp.export_gds(device, file=gds_file)
fp.plot(device)
# S-Parameters Export
SimFDTD(device=MMI, file_name="MMI", time=30000, n_modes=[1,2])
