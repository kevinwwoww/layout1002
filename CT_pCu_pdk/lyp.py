from pathlib import Path
from fnpcell import all as fp

from CT_pCu_pdk.technology import get_technology


def main():
    lyp_file = Path(__file__).with_name("CT_pCu_pdk.lyp")

    fp.export_lyp(get_technology(), file=lyp_file)


if __name__ == "__main__":
    main()
