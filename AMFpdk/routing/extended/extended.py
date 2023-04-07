from dataclasses import dataclass
from numbers import Number
from typing import List, Mapping, Tuple, Optional
from fnpcell import all as fp

from AMFpdk.technology import get_technology
from AMFpdk.components.straight.straight import Straight
from AMFpdk.routing.auto_transitioned.auto_transitioned import AutoTransitioned


@dataclass(eq=False)
class Extended(fp.PCell):
    """
      Attributes:
        device: device whose ports need to be extended
        lengths: dict with port name as key, length as value, "*" means every other port
        waveguide_type: type of generated waveguide
    """
    device: fp.IDevice = fp.DeviceParam()
    lengths: Mapping[str, float] = fp.MappingParam(K=str, V=Number, immutable=True)
    waveguide_type: Optional[fp.IWaveguideType] = fp.WaveguideTypeParam(required=False)

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        device = self.device
        lengths = self.lengths
        waveguide_type = self.waveguide_type
        instance = device if waveguide_type is None else AutoTransitioned(device=device, waveguide_types={key: waveguide_type for key in lengths})

        joints: List[fp.IOwnedTerminal, fp.IOwnedTerminal] = []
        straight_ports: List[fp.IOwnedTerminal] = []
        for port in instance.ports:
            if isinstance(port, fp.IOwnedPort) and not port.disabled:
                length = lengths.get(port.name) or lengths.get("*")
                if length is None:
                    if waveguide_type is None:
                        length -= fp.distance_between(device[port.name].position, instance[port.name].position)
                    assert length > 0 or fp.is_zero(length), f"extend length of {port.name} is too short"
                    if length > 0:
                        s = Straight(length=length, waveguide_type=port.waveguide_type)
                        joints.append(port <= s["op_0"])
                        port_name = port.name
                        straight_ports.append(s["op_1"].with_name(fp.Hidden(port_name) if port.hidden else port_name))

        used_port_names = set(port.name for port in straight_ports)
        unused_ports = [port for port in instance.ports if port.name not in used_port_names]
        connected = fp.Connected(
            joints=joints,
            ports=straight_ports + unused_ports,
        )
        insts += connected
        ports += connected.ports
        return insts, elems, ports


if __name__ == "__main__":
    from AMFpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()
    TECH = get_technology()

    from AMFpdk.components.mmi.mmi import MMI

    library += Extended(device=MMI(waveguide_type=TECH.WG.RIB.C.WIRE), lengths={"op_0": 30, "*": 10})

    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
