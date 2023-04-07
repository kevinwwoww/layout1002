# Generated from C:\photoCAD\layout1002\CT_pCu_pdk\technology\layers.csv

from fnpcell.pdk.technology.all import Layer, LayerEnum, Process, ProcessEnum, Purpose, PurposeEnum


class PROCESS(ProcessEnum):
    Hard_Mask_WG = Process(275, 'Hard_Mask_WG')
    Rib_WG = Process(406, 'Rib_WG')
    Strip_WG = Process(407, 'Strip_WG')
    SiN_WG = Process(263, 'SiN_WG')
    P = Process(256, 'P')
    N = Process(257, 'N')
    Pp = Process(258, 'Pp')
    Np = Process(259, 'Np')
    Ppp = Process(260, 'Ppp')
    Npp = Process(261, 'Npp')
    Ge_PD_NIP = Process(262, 'Ge_PD_NIP')
    Ge_Window = Process(264, 'Ge_Window')
    GeNp = Process(265, 'GeNp')
    GePp = Process(266, 'GePp')
    Nm = Process(417, 'Nm')
    Pm = Process(418, 'Pm')
    Contact_Si = Process(268, 'Contact_Si')
    Contact_Ge = Process(35, 'Contact_Ge')
    BEOL_Nlt0_removal = Process(283, 'BEOL_Nlt0_removal')
    M1 = Process(6, 'M1')
    BEOL_Nlt1_removal = Process(289, 'BEOL_Nlt1_removal')
    Via1 = Process(85, 'Via1')
    BEOL_Nlt2_removal = Process(290, 'BEOL_Nlt2_removal')
    M2 = Process(86, 'M2')
    BEOL_Nlt3_removal = Process(291, 'BEOL_Nlt3_removal')
    Via2 = Process(419, 'Via2')
    TaN_heater = Process(398, 'TaN_heater')
    Pad = Process(7, 'Pad')
    PadAl = Process(145, 'PadAl')
    Passivation_SiN_removal = Process(483, 'Passivation_SiN_removal')
    V_groove = Process(409, 'V_groove')
    Deep_Trench = Process(404, 'Deep_Trench')
    FLYLINE = Process(91, 'Fly Line')
    ERROR = Process(92, 'Error')
    PINREC = Process(70, 'Pin rectengle, fpr LVS, DRC')
    FIBREC = Process(71, 'Fiber rectangle, for LVS, DRC')
    FIBTGT = Process(72, 'Fiber target for LVS')
    DEVREC = Process(80, 'Device rectangle, for LVS, DRC')
    PAYLOAD = Process(50, 'Design area')
    IOPORT = Process(60, 'Optical port, for testing')
    TEXT = Process(56, 'Text layer, not to print on wafer')


class PURPOSE(PurposeEnum):
    DRW = Purpose(0, 'DRW')
    MARK = Purpose(35, 'Mark')
    NOTE = Purpose(30, 'Note')
    HM_WG = Purpose(31, 'Hard Mask WG')
    Rib = Purpose(32, 'Rib')
    Strip = Purpose(33, 'Strip')
    HM_PC = Purpose(34, 'Hard Mask PC')
    Si_PC = Purpose(36, 'Si PC')
    SiN = Purpose(37, 'SiN')
    TEXT = Purpose(41, 'Text')
    OREC = Purpose(21, 'Optical')
    EREC = Purpose(22, 'Electrical')


class LAYER(LayerEnum):
    Hard_Mask_WG = Layer(PROCESS.Hard_Mask_WG, PURPOSE.DRW, 'Define all WG( GC/slab/strip)')
    Rib_WG = Layer(PROCESS.Rib_WG, PURPOSE.DRW, '80nm etch (need to protect GC/strip WG)')
    Strip_WG = Layer(PROCESS.Strip_WG, PURPOSE.DRW, '150nm etch (need to protect GC/strip WG)')
    SiN_WG = Layer(PROCESS.SiN_WG, PURPOSE.DRW, '400nm SiN')
    P = Layer(PROCESS.P, PURPOSE.DRW, '')
    N = Layer(PROCESS.N, PURPOSE.DRW, '')
    Pp = Layer(PROCESS.Pp, PURPOSE.DRW, '')
    Np = Layer(PROCESS.Np, PURPOSE.DRW, '')
    Ppp = Layer(PROCESS.Ppp, PURPOSE.DRW, '')
    Npp = Layer(PROCESS.Npp, PURPOSE.DRW, '')
    Ge_PD_NIP = Layer(PROCESS.Ge_PD_NIP, PURPOSE.DRW, 'for vertical Ge PD P+')
    Ge_Window = Layer(PROCESS.Ge_Window, PURPOSE.DRW, 'Ge epi growth')
    GeNp = Layer(PROCESS.GeNp, PURPOSE.DRW, 'Lateral Ge PD N+')
    GePp = Layer(PROCESS.GePp, PURPOSE.DRW, 'Lateral Ge PD P+/Vertical Ge PD N+')
    Nm = Layer(PROCESS.Nm, PURPOSE.DRW, 'implant for high performance modulator')
    Pm = Layer(PROCESS.Pm, PURPOSE.DRW, 'implant for high performance modulator')
    Contact_Si = Layer(PROCESS.Contact_Si, PURPOSE.DRW, '0.6um*0.6um W-contact array')
    Contact_Ge = Layer(PROCESS.Contact_Ge, PURPOSE.DRW, '0.6um*0.6um W-contact array')
    BEOL_Nlt0_removal = Layer(PROCESS.BEOL_Nlt0_removal, PURPOSE.DRW, 'remove 100nm BEOL SiN ')
    M1 = Layer(PROCESS.M1, PURPOSE.DRW, '0.6um')
    BEOL_Nlt1_removal = Layer(PROCESS.BEOL_Nlt1_removal, PURPOSE.DRW, 'remove 100nm BEOL SiN ')
    Via1 = Layer(PROCESS.Via1, PURPOSE.DRW, '0.6um*0.6um Cu-via')
    BEOL_Nlt2_removal = Layer(PROCESS.BEOL_Nlt2_removal, PURPOSE.DRW, 'remove 100nm BEOL SiN ')
    M2 = Layer(PROCESS.M2, PURPOSE.DRW, '1.2um')
    BEOL_Nlt3_removal = Layer(PROCESS.BEOL_Nlt3_removal, PURPOSE.DRW, 'remove 100nm BEOL SiN ')
    Via2 = Layer(PROCESS.Via2, PURPOSE.DRW, 'min DR is 4um*4um and 2um gap')
    TaN_heater = Layer(PROCESS.TaN_heater, PURPOSE.DRW, '120nm')
    Pad = Layer(PROCESS.Pad, PURPOSE.DRW, 'passivation')
    PadAl = Layer(PROCESS.PadAl, PURPOSE.DRW, '2um bigger than Pad, 1.2um thick')
    Passivation_SiN_removal = Layer(PROCESS.Passivation_SiN_removal, PURPOSE.DRW, 'etch all SiN at GC region')
    V_groove = Layer(PROCESS.V_groove, PURPOSE.DRW, 'wet etch')
    Deep_Trench = Layer(PROCESS.Deep_Trench, PURPOSE.DRW, 'etch to 120um Si substate')
    FLYLINE_MARK = Layer(PROCESS.FLYLINE, PURPOSE.MARK, 'Flyline for insufficient space in AutoLink')
    ERROR_MARK = Layer(PROCESS.ERROR, PURPOSE.MARK, 'Error mark')
    PINREC_NOTE = Layer(PROCESS.PINREC, PURPOSE.NOTE, 'Pin rectengle, fpr LVS, DRC')
    PINREC_HM_WG = Layer(PROCESS.PINREC, PURPOSE.HM_WG, 'Pin rectengle, fpr LVS, DRC')
    PINREC_Rib = Layer(PROCESS.PINREC, PURPOSE.Rib, 'Pin rectengle, fpr LVS, DRC')
    PINREC_Strip = Layer(PROCESS.PINREC, PURPOSE.Strip, 'Pin rectengle, fpr LVS, DRC')
    PINREC_HM_PC = Layer(PROCESS.PINREC, PURPOSE.HM_PC, 'Pin rectengle, fpr LVS, DRC')
    PINREC_Si_PC = Layer(PROCESS.PINREC, PURPOSE.Si_PC, 'Pin rectengle, fpr LVS, DRC')
    PINREC_SiN = Layer(PROCESS.PINREC, PURPOSE.SiN, 'Pin rectengle, fpr LVS, DRC')
    PINREC_TEXT = Layer(PROCESS.PINREC, PURPOSE.TEXT, 'Pin rectengle, fpr LVS, DRC')
    FIBREC_NOTE = Layer(PROCESS.FIBREC, PURPOSE.NOTE, 'Fiber rectangle, for LVS, DRC')
    FIBTGT_NOTE = Layer(PROCESS.FIBTGT, PURPOSE.NOTE, 'Fiber target for LVS')
    DEVREC_NOTE = Layer(PROCESS.DEVREC, PURPOSE.NOTE, 'Device rectangle, for LVS, DRC')
    PAYLOAD_NOTE = Layer(PROCESS.PAYLOAD, PURPOSE.NOTE, 'Design area')
    IOPORT_OREC = Layer(PROCESS.IOPORT, PURPOSE.OREC, 'Optical port, for testing')
    IOPORT_EREC = Layer(PROCESS.IOPORT, PURPOSE.EREC, 'Electrical port, for testing')
    TEXT_NOTE = Layer(PROCESS.TEXT, PURPOSE.NOTE, 'Text layer, not to print on wafer')