from fnpcell import all as fp
from AMFpdk_3_5_Cband_0420.technology import get_technology


if __name__ == "__main__":
    fp.util.export_svrf_template(get_technology())
