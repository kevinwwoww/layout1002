from .auto_link import LINKING_POLICY
from .auto_transition import AUTO_TRANSITION
from .auto_vias import AUTO_VIAS
from .bands import BAND
from .device import DEVICE
from .display import DISPLAY
from .fitting_function import FITTING_FUNCTION
from .gdsii import GDSII
from .label import LABEL
from .layers import LAYER, PROCESS, PURPOSE
from .linker import LINKER
from .metal import METAL
from .metrics import METRICS
from .terminal import PIN, PORT
from .vias import VIAS
from .wg import WG
from .resources import RESOURCE


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
    VIAS = VIAS
    DISPLAY = DISPLAY
    AUTO_TRANSITION = AUTO_TRANSITION
    AUTO_VIAS = AUTO_VIAS
    LINKING_POLICY = LINKING_POLICY
    FITTING_FUNCTION = FITTING_FUNCTION
    LINKER = LINKER
    LINK_BETWEEN = LINKER
