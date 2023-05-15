from fnpcell import all as fp


class PCellBase(fp.PCell):
    name: str = fp.NameParam(prefix="", hash=False, compare=False)
