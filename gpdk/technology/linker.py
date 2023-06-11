from dataclasses import dataclass
from typing import Any, Optional

from fnpcell import all as fp
from fnpcell.pdk.technology import all as fpt


class LINKER:
    @dataclass(eq=False)
    class SWG_WIRE_FWG_EULER(fpt.WaveguideBetween, fp.PCell):
        start: fpt.IPort = fp.Param(type=fpt.IPort)
        end: fpt.IPort = fp.Param(type=fpt.IPort)
        waypoints: fpt.IWaypoints = fp.ListParam(default=(), immutable=True)
        waylines: fpt.IWaylines = fp.ListParam(default=(), immutable=True)
        target_length: Optional[float] = fp.PositiveFloatParam(required=False)
        flyline_layer: Optional[fpt.ILayer] = fp.LayerParam(required=False)
        link_type: fp.IWaveguideType = fp.Param(locked=True)
        bend_factory: fp.IBendWaveguideFactory = fp.Param(locked=True)

        def _default_link_type(self):
            from . import get_technology

            TECH = get_technology()
            return TECH.WG.SWG.C.WIRE

        def _default_bend_factory(self):
            from . import get_technology

            TECH = get_technology()
            return TECH.WG.FWG.C.WIRE.BEND_EULER

        @property
        def generated_link(self) -> fpt.IWaveguideBetween:
            link = fp.LinkBetween(
                self.start,
                self.end,
                waypoints=self.waypoints,
                waylines=self.waylines,
                target_length=self.target_length,
                link_type=self.link_type,
                bend_factory=self.bend_factory,
                flyline_layer=self.flyline_layer,
            )
            return link

        def build(self):
            inst_set, elem_set, port_set = super().build()

            inst_set += self.generated_link
            port_set += self.generated_link.ports

            return inst_set, elem_set, port_set

        def with_environment(self, flyline_layer: Optional[fpt.ILayer] = None, **kwargs: Any):
            if self.flyline_layer is None:
                return self.updated(flyline_layer=flyline_layer)
            return self

    @dataclass(eq=False)
    class SWG_EXPANDED_MWG_EULER(fpt.WaveguideBetween, fp.PCell):
        start: fpt.IPort = fp.Param(type=fpt.IPort)
        end: fpt.IPort = fp.Param(type=fpt.IPort)
        waypoints: fpt.IWaypoints = fp.ListParam(default=(), immutable=True)
        waylines: fpt.IWaylines = fp.ListParam(default=(), immutable=True)
        target_length: Optional[float] = fp.PositiveFloatParam(required=False)
        flyline_layer: Optional[fpt.ILayer] = fp.LayerParam(required=False)
        link_type: fp.IWaveguideType = fp.Param(locked=True)
        bend_factory: fp.IBendWaveguideFactory = fp.Param(locked=True)

        def _default_link_type(self):
            from . import get_technology

            TECH = get_technology()
            return TECH.WG.SWG.C.EXPANDED

        def _default_bend_factory(self):
            from . import get_technology

            TECH = get_technology()
            return TECH.WG.MWG.C.WIRE.BEND_EULER

        @property
        def generated_link(self) -> fpt.IWaveguideBetween:
            link = fp.LinkBetween(
                self.start,
                self.end,
                waypoints=self.waypoints,
                waylines=self.waylines,
                target_length=self.target_length,
                link_type=self.link_type,
                bend_factory=self.bend_factory,
                flyline_layer=self.flyline_layer,
            )
            return link

        def build(self):
            inst_set, elem_set, port_set = super().build()

            inst_set += self.generated_link
            port_set += self.generated_link.ports

            return inst_set, elem_set, port_set

        def with_environment(
            self,
            flyline_layer: Optional[fpt.ILayer] = None,
            linking_policy: Optional[fpt.LinkingPolicy] = None,
            link_type: Optional[fpt.IWaveguideType] = None,
            straight_factory: Optional[fpt.IStraightWaveguideFactory] = None,
            bend_factory: Optional[fpt.IBendWaveguideFactory] = None,
            **kwargs: Any
        ):
            if self.flyline_layer is None:
                return self.updated(flyline_layer=flyline_layer)
            return self
