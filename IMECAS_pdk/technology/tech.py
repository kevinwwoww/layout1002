from IMECAS_pdk.technology.auto_link import LINKING_POLICY
from IMECAS_pdk.technology.auto_transition import AUTO_TRANSITION
from IMECAS_pdk.technology.bands import BAND
from IMECAS_pdk.technology.device import DEVICE
from IMECAS_pdk.technology.display import DISPLAY
from IMECAS_pdk.technology.gdsii import GDSII
from IMECAS_pdk.technology.label import LABEL
from IMECAS_pdk.technology.layers import LAYER, PROCESS, PURPOSE
from IMECAS_pdk.technology.metal import METAL
from IMECAS_pdk.technology.metrics import METRICS
from IMECAS_pdk.technology.terminal import PIN, PORT
from IMECAS_pdk.technology.wg import WG
from IMECAS_pdk.technology.resource import RESOURCE


class TECH:
    RESOURCE = RESOURCE
    GDSII = GDSII
    METRICS = METRICS
    PIN = PIN
    PORT = PORT
    LABEL = LABEL
    PROCESS = PROCESS
    PURPOSE = PURPOSE
    LAYER = LAYER
    DEVICE = DEVICE
    BAND = BAND
    WG = WG
    METAL = METAL
    DISPLAY = DISPLAY
    AUTO_TRANSITION = AUTO_TRANSITION
    LINKING_POLICY = LINKING_POLICY


