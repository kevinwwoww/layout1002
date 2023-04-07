from fnpcell import all as fp
from layout01.technology import get_technology


if __name__ == "__main__":
    from pathlib import Path

    lyp_file = Path(__file__).with_name("layout01.lyp")

    fp.export_lyp(get_technology(), file=lyp_file)
