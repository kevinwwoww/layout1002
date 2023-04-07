from dataclasses import dataclass
from fnpcell.pdk.technology import all as fpt
from CT_Al_pdk.technology.interfaces import CrackedMetalLineType


class METAL:
    @fpt.classconst
    @classmethod
    def metal_stack(cls) -> fpt.MetalStack:
        from CT_Al_pdk.technology import get_technology

        TECH = get_technology()
        return fpt.MetalStack(
            layers=[
                TECH.LAYER.first_thick_metal,
                TECH.LAYER.Top_Metal,
            ],
            connectivity={
                TECH.LAYER.first_thick_metal: [TECH.LAYER.Via1],
                TECH.LAYER.Top_Metal: [TECH.LAYER.Top_Via],
            }
        )

    @staticmethod
    def from_single_layer(layer: fpt.ILayer) -> fpt.IMetalLineType:
        from CT_Al_pdk.technology import get_technology

        TECH = get_technology()
        if layer == TECH.LAYER.first_thick_metal:
            return TECH.METAL.first_thick_metal.W20
        elif layer == TECH.LAYER.Top_Metal:
            return TECH.METAL.Top_Metal.W20
        else:
            raise ValueError(f"MetalLineType for layer [{layer}] not found")

    @fpt.hash_code
    @dataclass(frozen=True)
    class first_thick_metal(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from CT_Al_pdk.technology import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.first_thick_metal])

        @fpt.classconst
        @classmethod
        def W10(cls):
            return cls(line_width=10)

        @fpt.classconst
        @classmethod
        def W20(cls):
            return cls(line_width=20)

        @fpt.classconst
        @classmethod
        def W40(cls):
            return cls(line_width=40)

        @fpt.classconst
        @classmethod
        def W80(cls):
            return cls(line_width=80)

    @fpt.hash_code
    @dataclass(frozen=True)
    class Top_Metal(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from CT_Al_pdk.technology import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.Top_Metal])

        @fpt.classconst
        @classmethod
        def W10(cls):
            return cls(line_width=10)

        @fpt.classconst
        @classmethod
        def W20(cls):
            return cls(line_width=20)

        @fpt.classconst
        @classmethod
        def W40(cls):
            return cls(line_width=40)

        @fpt.classconst
        @classmethod
        def W80(cls):
            return cls(line_width=80)

    @fpt.hash_code
    @dataclass(frozen=True)
    class Pad(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from CT_Al_pdk.technology import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.Pad])

        @fpt.classconst
        @classmethod
        def W10(cls):
            return cls(line_width=10)

        @fpt.classconst
        @classmethod
        def W20(cls):
            return cls(line_width=20)

        @fpt.classconst
        @classmethod
        def W40(cls):
            return cls(line_width=40)

        @fpt.classconst
        @classmethod
        def W80(cls):
            return cls(line_width=80)


