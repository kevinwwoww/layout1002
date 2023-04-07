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
                TECH.LAYER.M1_DRW,
            ],
            connectivity={
                TECH.LAYER.M1_DRW: [TECH.LAYER.PCON, TECH.LAYER.GEPCON, TECH.LAYER.TIN, TECH.LAYER.PAD],
            },
        )

    @staticmethod
    def from_single_layer(layer: fpt.ILayer) -> fpt.IMetalLineType:
        from . import get_technology

        TECH = get_technology()
        if layer == TECH.LAYER.M1:
            return TECH.METAL.M1.W20

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

