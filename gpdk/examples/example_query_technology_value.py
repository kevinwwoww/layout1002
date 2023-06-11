from fnpcell import all as fp
from gpdk.technology import get_technology


if __name__ == "__main__":
    TECH = get_technology()
    # =============================================================
    wgt1 = fp.query_technology_value(TECH, path="TECH.WG.SWG.C.WIRE")
    wgt2 = fp.query_technology_value(path="TECH.WG.SWG.C.WIRE")
    wgt3 = fp.query_technology_value(path="WG.SWG.C.WIRE")
    wgt4 = TECH.WG.SWG.C.WIRE

    assert wgt1 == wgt2 == wgt3 == wgt4, "All waveguide types should be equal"
    # =============================================================
    print("Technology value query executed successfully")
