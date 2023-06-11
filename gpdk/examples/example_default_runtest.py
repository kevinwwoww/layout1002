from dataclasses import dataclass
from fnpcell import all as fp
from gpdk.technology import get_technology

class test_default(fp.PCell):
    a: float = fp.FloatParam()
    b: float = fp.FloatParam()
    c: float = fp.FloatParam()
    d: float = fp.FloatParam()
    e: float = fp.FloatParam()
    f: float = fp.FloatParam()

    # @fp.cache()
    def _default_a(self):
        print("test_a")
        return 1

    # @fp.cache()
    def _default_b(self):
        print("test_b")
        return self.a + 3

    # @fp.cache()
    def _default_c(self):
        print("test_c")

        return self.d * self.b + self.a

    def _default_d(self):
        print("test_d")
        return 5 * self.f

    def _default_e(self):
        print("test_e")
        return self.c * 2 + self.f

    # @fp.cache()
    def _default_f(self):
        print("test_f")
        return 2



    def build(self):
        insts, elems, ports = super().build()

        print("build")

        test = fp.el.Line(length=self.a, stroke_width=self.b, final_stroke_width=self.c, layer=get_technology().LAYER.PINREC_TEXT).extension(10,10)

        test2 = fp.el.Line(length=self.d, stroke_width=self.e, final_stroke_width=self.f, layer=get_technology().LAYER.ERROR_MARK).translated(10, 10)

        elems += test, test2

        print(self.d, self.e)



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




