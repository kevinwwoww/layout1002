import math
from typing import Any, List, Optional, cast

from fnpcell import all as fp
from IMECAS_pdk.components.straight.straight import Straight


def transition_start(
    TECH: Any,
    content: List[fp.ICellRef],
    *,
    start: fp.IPort,
    final_type: fp.IWaveguideType,
) -> fp.IPort:
    initial_type = start.waveguide_type

    if initial_type != final_type:
        transition, (port_in, port_out) = TECH.AUTO_TRANSITION.DEFAULT[initial_type >> final_type]
        transition = fp.place(transition, port_in, at=start)
        content.append(transition)
        start = cast(fp.IPort, transition[port_out])

    return start


def transition_end(
    TECH: Any,
    content: List[fp.ICellRef],
    *,
    end: fp.IPort,
    initial_type: fp.IWaveguideType,
) -> fp.IPort:
    final_type = end.waveguide_type

    if initial_type != final_type:
        transition, (port_in, port_out) = TECH.AUTO_TRANSITION.DEFAULT[initial_type >> final_type]
        transition = fp.place(transition, port_out, at=end)
        content.append(transition)
        end = cast(fp.IPort, transition[port_in])

    return end


def straight(
    TECH: Any,
    content: List[fp.ICellRef],
    *,
    start: fp.IPort,
    link_type: Optional[fp.IWaveguideType] = None,
    length: float,
    end_type: Optional[fp.IWaveguideType] = None,
) -> fp.IOwnedPort:
    initial_type = start.waveguide_type
    if link_type is None:
        link_type = initial_type
    if end_type is None:
        end_type = link_type

    x, y = start.position
    orientation = start.orientation

    end = None
    if end_type != link_type:
        end = fp.Port(
            name="END",
            position=(x + length * math.cos(orientation), y + length * math.sin(orientation)),
            orientation=fp.normalize_angle(orientation - math.pi),
            waveguide_type=end_type,
        )
        port = transition_end(TECH, content, end=end, initial_type=link_type)
        length -= fp.distance_between(port.position, end.position)
        end = content[-1]["op_1"]

    if initial_type != link_type:
        port = transition_start(TECH, content, start=start, final_type=link_type)
        length -= fp.distance_between(port.position, start.position)
        start = port

    straight = Straight(
        name="s",
        length=length,
        waveguide_type=link_type,
        transform=fp.rotate(radians=orientation).translate(*start.position),
    )
    content.append(straight)

    return cast(fp.IOwnedPort, end or straight["op_1"])


def bend(
    TECH: Any,
    content: List[fp.ICellRef],
    *,
    start: fp.IPort,
    radians: float,
    bend_factory: Optional[fp.IBendWaveguideFactory] = None,
    end_type: Optional[fp.IWaveguideType] = None,
) -> fp.IOwnedPort:

    initial_type = start.waveguide_type
    start_offset = 0
    end_offset = 0

    if bend_factory is None:
        bend_factory = start.waveguide_type.bend_factory

    bend, _, (port_in, _) = bend_factory(central_angle=radians)
    bend_type = cast(fp.IPort, bend[port_in]).waveguide_type

    if initial_type != bend_type:
        transition_end = transition_start(TECH, content, start=start, final_type=bend_type)
        start_offset += fp.distance_between(start.position, transition_end.position)
        start = transition_end

    bend, _, (port_in, port_out) = bend_factory(central_angle=radians)
    # bend = bend.rotated(radians=start.orientation).translated(*start.position)
    bend = fp.place(bend, port_in, at=start)

    content.append(bend)

    if end_type is not None and end_type != bend_type:
        start = bend[port_out]
        transition_end = transition_start(TECH, content, start=start, final_type=end_type)
        end_offset += fp.distance_between(start.position, transition_end.position)
        start = transition_end

    return bend[port_out]
