import math
from dataclasses import dataclass
from fnpcell import all as fp
from gpdk import all as pdk


@dataclass(frozen=True)
class Info:
    name: str
    x: float
    y: float
    orientation: float


if __name__ == "__main__":
    mmi = pdk.Mmi(n_inputs=2, n_outputs=3)
    _ = fp.expr.ImplicitTarget()

    left_ports = mmi.ports.where(_.orientation == math.pi).order_by(_.y, reverse=True)
    print("left:   ", [(it.name, it.position, it.orientation) for it in left_ports])

    right_ports = mmi.ports.where(_.orientation == 0).order_by(_.y)
    print("right:  ", [(it.name, it.position, it.orientation) for it in right_ports])

    # here we use `&` for boolean `and` since we cannot overload `and` in python.
    # For the same reason, `|` is used for boolean `or`
    special_ports = mmi.ports.where((_.x > _.y) & (_.position[1] < 0)).order_by(_.y)
    print("special:", [(it.name, it.position, it.orientation) for it in special_ports])

    special_ports = mmi.ports.where((_.x + _.y) == 28.0)
    print("x+y==28:", [(it.name, it.position, it.orientation) for it in special_ports])

    # `sin`` is not known by `fn.expr`, so we wrap it to make `fp.expr` happy
    sin = fp.expr.fn(math.sin)
    special_ports = mmi.ports.where(sin(_.orientation) == 1.0)
    print("sin== 1:", [(it.name, it.position, it.orientation) for it in special_ports])

    # `seq` here is just `tuple` in `fp.expr``, so `select` will return (name, position, orientation)
    seq = fp.expr.seq
    result = mmi.ports.where(round(sin(_.orientation), 3) == 0.0).select(seq(_.name, _.position, _.orientation))
    print("sin== 0:", result)

    # wrap `Info` to use it in `fp.expr`
    info = fp.expr.fn(Info)
    result = mmi.ports.where(_.name != "op_3").order_by(seq(_.x, _.y)).select(info(name=_.name, x=_.x, y=_.position[1], orientation=_.orientation))
    print("select :", result)

    # slice
    result = mmi.ports.where(_.name != "op_3").order_by(seq(_.x, _.y))[1:-1].select(info(name=_.name, x=_.x, y=_.position[1], orientation=_.orientation))
    print("select :", result)

    # fp.plot(mmi)
