from fnpcell.pdk.technology.all import BandEnum, Band


class BAND(BandEnum):
    O = Band((1260, 1360), "Original Band")
    E = Band((1360, 1460), "Extended-wavelength Band")
    S = Band((1460, 1530), "Short-wavelength Band")
    C = Band((1530, 1565), "Conventional Band")
    L = Band((1565, 1625), "Long-wavelength Band")
    U = Band((1565, 1675), "Ultra-long-wavelength Band")
