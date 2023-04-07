from fnpcell.pdk.technology.all import Layer, Process, Purpose
from gpdk.technology.tech import TECH as GPDK_TECH


class PROCESS(GPDK_TECH.PROCESS):
    TIN = Process(131, "TiN Metal heater")


class PURPOSE(GPDK_TECH.PURPOSE):
    NOTE = Purpose(40, "Note")


class LAYER(GPDK_TECH.LAYER):
    TIN_DRW = Layer(PROCESS.TIN, PURPOSE.DRW, "TiN heater")

    DEVREC_NOTE = Layer(PROCESS.DEVREC, PURPOSE.NOTE, "Device rectangle, for LVS, DRC")
