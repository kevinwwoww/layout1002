from fnpcell.pdk.technology.all import BandEnum, Band


class BAND(BandEnum):
    O = Band((1260, 1360), "Original Band")
    C = Band((1530, 1565), "Conventional Band")

