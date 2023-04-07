from pathlib import Path

from fnpcell import all as fp
from layout01.circuits.circuit_01.circuit_01 import Circuit01
from layout01.technology import get_technology


def build_circuit_01():
    print("build 01")
    TECH = get_technology()

    fwg_type = TECH.WG.FWG.C.WIRE

    cell = Circuit01(
        name="01",
        gc_spacing=100,
        ring_radius=50,
        swg_spacing=30,
        swg_length=50,
        fwg_type=fwg_type,
        swg_type=TECH.WG.SWG.C.WIRE,
        mwg_type=TECH.WG.MWG.C.WIRE,
    )
    import time

    time.sleep(20)

    return cell


if __name__ == "__main__":
    from layout01.technology import get_technology

    TECH = get_technology()
    gds_file = TECH.RESOURCE.CIRCUIT_BUILD_FOLDER / Path(__file__).with_suffix(".gds").name

    cell = build_circuit_01()
    fp.export_gds(cell, file=gds_file)
