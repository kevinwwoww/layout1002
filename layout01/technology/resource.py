from pathlib import Path
from gpdk.technology.tech import TECH as GPDK_TECH


LAYOUT_01_FOLDER = Path(__file__).parent.parent


class RESOURCE(GPDK_TECH.RESOURCE):
    CIRCUIT_BUILD_FOLDER = LAYOUT_01_FOLDER / "build" / "circuits"


if __name__ == "__main__":
    print(RESOURCE.CIRCUIT_BUILD_FOLDER)
