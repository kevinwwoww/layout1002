from dataclasses import dataclass
from typing import List, Tuple

from fnpcell import all as fp


@dataclass(frozen=True)
class SamplerPeriodic:
    period: float
    reserved_ends: Tuple[float, float] = (0, 0)

    def __post_init__(self):
        start, end = self.reserved_ends
        assert start >= 0 and end >= 0, "requires s >= 0 and e >= 0 where reserved_ends = (s, e), got: {self.reserved_ends}"

    def __call__(self, curve: fp.ICurve) -> Tuple[fp.SampleInfo, ...]:
        period = self.period
        start, end = self.reserved_ends

        total_length = curve.curve_length
        end = total_length - end
        result: List[fp.SampleInfo] = []
        while start <= end:
            result.append(curve.sample_at(start))
            start += period

        return tuple(result)
