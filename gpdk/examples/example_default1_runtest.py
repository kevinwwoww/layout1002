from dataclasses import dataclass
from fnpcell import all as fp
from gpdk.technology import get_technology

class test_default(fp.PCell):
    a: float = fp.FloatParam(default=1)
    b: float = fp.FloatParam(default=2)
    c: float = fp.FloatParam(default=3)
    d: float = fp.FloatParam(default=4)
    e: float = fp.FloatParam(default=5)
    f: float = fp.FloatParam()

    @fp.cache()
    def _default_f(self):
        print("test_f")
        return 6



    def build(self):
        insts, elems, ports = super().build()



        test = fp.el.Line(length=self.a, stroke_width=self.b, final_stroke_width=self.c, layer=get_technology().LAYER.PINREC_TEXT)

        test2 = fp.el.Line(length=self.d, stroke_width=self.e, final_stroke_width=self.f, layer=get_technology().LAYER.ERROR_MARK).translated(10, 10)

        elems += test, test2





        return insts, elems, ports



if __name__ == "__main__":
    from gpdk.components import all as components
    from gpdk.util.path import local_output_file

    gds_file = local_output_file(__file__).with_suffix(".gds")
    library = fp.Library()

    TECH = get_technology()
    # =======================================================================
    # fmt: off

    library += test_default()


    # fmt: on
    # =============================================================

    fp.plot(library)




