from fnpcell import all as fp
from gpdk.technology import get_technology


if __name__ == "__main__":
    fp.util.export_svrf_template(get_technology())
