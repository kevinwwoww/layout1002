from pathlib import Path
from fnpcell import all as fp

from IMECAS_SiN_pdk_1_0_0.technology import get_technology


def main():
    lyp_file = Path(__file__).with_name("IMECAS_SiN_pdk_1_0_0.lyp")

    fp.export_lyp(get_technology(), file=lyp_file)


if __name__ == "__main__":
    main()
