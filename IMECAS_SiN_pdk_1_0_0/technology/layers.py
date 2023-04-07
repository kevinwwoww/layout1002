# Generated from C:\photoCAD\layout1002\IMECAS_SiN_pdk_1_0_0\technology\layers.csv

from fnpcell.pdk.technology.all import Layer, LayerEnum, Process, ProcessEnum, Purpose, PurposeEnum

class PROCESS(ProcessEnum):
    SIN = Process(50, 'Full etch')
    BB = Process(120, 'Define design boundary')
    DOC = Process(1000, 'Only for layout recognization, will not appear on mask')
    PINREC = Process(1002, 'Port recognization')
    FLYLINE = Process(91, 'Fly line')
    ERROR = Process(92, 'Error')

class PURPOSE(PurposeEnum):
    COR = Purpose(2, 'Waveguide core')
    CLD = Purpose(3, 'Waveguide cladding')
    TRE = Purpose(4, 'Waveguide trench')
    DRW = Purpose(0, 'Drawing')
    MARK = Purpose(35, 'Mark')

class LAYER(LayerEnum):
    SINCOR = Layer(PROCESS.SIN, PURPOSE.COR, '200nm Full Etch SiN waveguide core')
    SINCLD = Layer(PROCESS.SIN, PURPOSE.CLD, '200nm Full Etch SiN waveguide cladding')
    SINTCH = Layer(PROCESS.SIN, PURPOSE.TRE, '200nm Full Etch SiN waveguide trench')
    BB = Layer(PROCESS.BB, PURPOSE.DRW, 'Define design boundary')
    DOC = Layer(PROCESS.DOC, PURPOSE.DRW, 'Only for layout recognization, will not appear on mask')
    PINREC = Layer(PROCESS.PINREC, PURPOSE.DRW, 'Port recognization')
    FLYLINE_MARK = Layer(PROCESS.FLYLINE, PURPOSE.MARK, 'Flyline for insufficient space in AutoLink(from LDA)')
    ERROR_MARK = Layer(PROCESS.ERROR, PURPOSE.MARK, 'Error mark(from LDA)')
