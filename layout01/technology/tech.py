from gpdk.technology.tech import TECH as GPDK_TECH

from .display import DISPLAY
from .device import DEVICE
from .layers import LAYER, PROCESS, PURPOSE
from .metrics import METRICS
from .terminal import PORT
from .wg import WG
from .label import LABEL
from .resource import RESOURCE


class TECH(GPDK_TECH):
    METRICS = METRICS
    DEVICE = DEVICE
    PORT = PORT
    LABEL = LABEL
    PROCESS = PROCESS
    PURPOSE = PURPOSE
    LAYER = LAYER
    WG = WG
    DISPLAY = DISPLAY
    RESOURCE = RESOURCE
