from dataclasses import dataclass

from fnpcell.pdk.technology import all as fpt

from .interfaces import CrackedMetalLineType


class METAL:
    @fpt.classconst
    @classmethod
    def metal_stack(cls) -> fpt.MetalStack:
        from . import get_technology

        TECH = get_technology()
        return fpt.MetalStack(
            layers=[
                TECH.LAYER.MT_DRW,
                TECH.LAYER.M2_DRW,
                TECH.LAYER.M1_DRW,
            ],
            connectivity={
                TECH.LAYER.MT_DRW: [TECH.LAYER.VIA2_DRW],
                TECH.LAYER.M2_DRW: [TECH.LAYER.VIA2_DRW, TECH.LAYER.VIA1_DRW],
                TECH.LAYER.M1_DRW: [TECH.LAYER.VIA1_DRW],
            },
        )

    @staticmethod
    def from_single_layer(layer: fpt.ILayer) -> fpt.IMetalLineType:
        from . import get_technology

        TECH = get_technology()
        if layer == TECH.LAYER.M1_DRW:
            return TECH.METAL.M1.W20
        elif layer == TECH.LAYER.M2_DRW:
            return TECH.METAL.M2.W20
        elif layer == TECH.LAYER.MT_DRW:
            return TECH.METAL.MT.W20
        else:
            raise ValueError(f"MetalLineType for layer [{layer}] not found")

    @fpt.hash_code
    @dataclass(frozen=True)
    class M1(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from . import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.M1_DRW])

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
            from . import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.M2_DRW])

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
    class MT(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from . import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.MT_DRW])

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
    class PASS_MT(CrackedMetalLineType):
        @fpt.classconst
        @classmethod
        def metal_stack(cls) -> fpt.MetalStack:
            from . import get_technology

            TECH = get_technology()
            return TECH.METAL.metal_stack.updated(layers=[TECH.LAYER.PASS_MT])

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
