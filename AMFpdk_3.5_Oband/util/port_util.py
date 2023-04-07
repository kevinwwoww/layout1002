import math
from fnpcell import all as fp


def get_left_ports(device: fp.ICellRef, reverse: bool = False):
    ports = [
        p
        for p in device.ports
        if isinstance(p, fp.IOwnedPort)
        and (fp.normalize_angle(p.orientation) > math.pi / 2 or fp.normalize_angle(p.orientation) < -math.pi / 2)
    ]
    ports.sort(key=lambda p: -p.position[1], reverse=reverse)
    return ports


def get_right_ports(device: fp.ICellRef, reverse: bool = False):
    ports = [
        p
        for p in device.ports
        if isinstance(p, fp.IOwnedPort) and -math.pi / 2 < fp.normalize_angle(p.orientation) < math.pi / 2
    ]
    ports.sort(key=lambda p: -p.position[1], reverse=reverse)
    return ports
