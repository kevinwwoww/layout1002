from pathlib import Path
from fnpcell import all as fp
from layout01.circuits.circuit_04.circuit_04 import Circuit04


def build_circuit_04():
    print("build 04")
    cell = Circuit04(
        name="04",
    )
    import time

    time.sleep(20)

    return cell


if __name__ == "__main__":
    from layout01.technology import get_technology

    TECH = get_technology()
    gds_file = TECH.RESOURCE.CIRCUIT_BUILD_FOLDER / Path(__file__).with_suffix(".gds").name

    cell = build_circuit_04()
    fp.export_gds(cell, file=gds_file)
