from dataclasses import dataclass
from fnpcell.pdk.technology import all as fpt
from CT_pCu_pdk.technology.interfaces import CrackedMetalLineType


class METAL:
    @fpt.classconst
    @classmethod
    def metal_stack(cls) -> fpt.MetalStack:
        from CT_pCu_pdk.technology import get_technology

        TECH = get_technology()
        return fpt.MetalStack(
            layers=[
                TECH.LAYER.M1,
                TECH.LAYER.M2,
                TECH.LAYER.PadAl,
            ],
            connectivity={
                TECH.LAYER.M1: [TECH.LAYER.Via1],
                TECH.LAYER.M2: [TECH.LAYER.Via1, TECH.LAYER.PadAl],
                TECH.LAYER.PadAl: [TECH.LAYER.M2]
            }
        )

    @staticmethod
    def from_single_layer(layer: fpt.ILayer) -> fpt.IMetalLineType:
        from CT_pCu_pdk.technology import get_technology

        TECH = get_technology()
        if layer == TECH.LAYER.M1:
            return TECH.METAL.M1.W20
        elif layer == TECH.LAYER.M2:
            return TECH.METAL.M2.W20
        elif layer == TECH.LAYER.PadAI:
            return TECH.METAL.PadAI.W20
        else:
            raise ValueError(f"MetalLineType for layer [{layer}] not found")

    @fpt.hash_code
    @dataclass(frozen=True)
    class M1(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from CT_pCu_pdk.technology import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.M1])

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
    class M2(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from CT_pCu_pdk.technology import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.M2])

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
            from CT_pCu_pdk.technology import get_technology

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

    @fpt.hash_code
    @dataclass(frozen=True)
    class PadAl(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from CT_pCu_pdk.technology import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.PadAl])

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
