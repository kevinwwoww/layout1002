from dataclasses import dataclass
from typing import List, Mapping, Tuple

from fnpcell import all as fp
from gpdk.technology import get_technology


@dataclass(eq=False)
class AutoTransitioned(fp.PCell):
    """
    Attributes:
        device: device whose ports need to be auto-transitioned
        waveguide_type: dict with port name as key, waveguide type as value, "*" means every other port

    Examples:
    ```python
    TECH = get_technology()
        device = AutoTransitioned(device=Mmi(waveguide_type=TECH.WG.FWG.C.WIRE), waveguide_types={"*": WG.SWG.C.WIRE})
    fp.plot(device)
    ```
    ![AutoTransitioned](images/auto_transitioned.png)
    """

    device: fp.IDevice = fp.DeviceParam()
    waveguide_types: Mapping[str, fp.IWaveguideType] = fp.MappingParam(K=str, V=fp.IWaveguideType, immutable=True)

    def build(self) -> Tuple[fp.InstanceSet, fp.ElementSet, fp.PortSet]:
        insts, elems, ports = super().build()
        TECH = get_technology()
        waveguide_types = self.waveguide_types
        joints: List[Tuple[fp.IOwnedTerminal, fp.IOwnedTerminal]] = []
        transition_ports: List[fp.IOwnedTerminal] = []
        for port in self.device.ports:
            if isinstance(port, fp.IOwnedPort) and not port.disabled:
                start_type = port.waveguide_type
                end_type = waveguide_types.get(port.name) or waveguide_types.get("*")
                if end_type is not None and start_type != end_type:
                    transition, (port_in, port_out) = TECH.AUTO_TRANSITION.DEFAULT[start_type >> end_type]
                    joints.append(port <= transition[port_in])
                    port_name = port.name
                    transition_ports.append(transition[port_out].with_name(fp.Hidden(port_name) if port.hidden and port_name else port_name))

        used_port_names = set(port.name for port in transition_ports)
        unused_ports = [port for port in self.device.ports if not port.disabled and port.name not in used_port_names]
        device = fp.Connected(
            joints=joints,
            ports=transition_ports + unused_ports,
        )
        insts += device
        ports += device.ports

        return insts, elems, ports


if __name__ == "__main__":
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =============================================================
    # fmt: off
    from gpdk.components.mmi.mmi import Mmi

    library += AutoTransitioned(device=Mmi(waveguide_type=TECH.WG.FWG.C.WIRE), waveguide_types={"*": TECH.WG.SWG.C.WIRE})

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    # fp.plot(library)
