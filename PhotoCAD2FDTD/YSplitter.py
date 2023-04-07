from fnpcell import all as fp
from gpdk import all as pdk
from gpdk.technology import get_technology
from os import path
from SimFDTD import SimFDTD
TECH = get_technology()
# ========================================================================= #
instSet, elemSet, portSet = fp.InstanceSet(), fp.ElementSet(), fp.PortSet()
# Call component
YS = pdk.YSplitter(waveguide_type=TECH.WG.FWG.C.WIRE, taper_length=5, bend_radius=5, out_degrees=90)
# Port extension
instSet += pdk.Extended(device=YS, lengths={"*": 1})
device = fp.Device(name="YS", content=instSet + elemSet, ports=portSet)
# Define the path of the .gds file
gds_file = path.join(path.dirname(__file__), "local", "Ysplitter.gds")
library = fp.Library()
library += device
# GDS export
fp.export_gds(library, file=gds_file)
fp.plot(library)
# S-Parameters Export
SimFDTD(device=YS, file_name="Ysplitter", cell_name="YS", time=30000, n_modes=[1])
