from dataclasses import dataclass
from fnpcell.pdk.technology import all as fpt
from AMFpdk_3_5_Oband.technology.interfaces import CrackedMetalLineType

class METAL:
    @fpt.classconst
    @classmethod
    def metal_stack(cls) -> fpt.MetalStack:
        from AMFpdk_3_5_Oband.technology import get_technology

        TECH = get_technology()
        return fpt.MetalStack(
            layers=[
                TECH.LAYER.MT1,
                TECH.LAYER.MT2,
            ],
            connectivity={
                TECH.LAYER.MT1: [TECH.LAYER.VIA1],
                TECH.LAYER.MT2: [TECH.LAYER.VIA1, TECH.LAYER.VIA2],
            }
        )

    @staticmethod
    def from_single_layer(layer: fpt.ILayer) -> fpt.IMetalLineType:
        from AMFpdk_3_5_Oband.technology import get_technology

        TECH = get_technology()
        if layer == TECH.LAYER.MT1:
            return TECH.METAL.M1.W20
        elif layer == TECH.LAYER.MT2:
            return TECH.METAL.M2.W20
        else:
            raise ValueError(f"MetalLineType for layer [{layer}] not found")

    @fpt.hash_code
    @dataclass(frozen=True)
    class MT1(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from AMFpdk_3_5_Oband.technology import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.MT1])

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
    class MT2(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from AMFpdk_3_5_Oband.technology import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.MT2])

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
        def W70(cls):
            return cls(line_width=70)

        @fpt.classconst
        @classmethod
        def W80(cls):
            return cls(line_width=80)

    @fpt.hash_code
    @dataclass(frozen=True)
    class PAD(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from AMFpdk_3_5_Oband.technology import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.PAD])

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

