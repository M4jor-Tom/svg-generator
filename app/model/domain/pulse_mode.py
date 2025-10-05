from pydantic import BaseModel

from util import DomUtil


class PulseMode(BaseModel):
    duration_s: float
    count: int

    def build_animation(self, from_value: str, to_value: str, animation_tag: str, animated_property: str) -> str:
        return DomUtil.build_element(animation_tag, {
            "attributeName": animated_property,
            "fill": "freeze",
            "dur": f"{self.duration_s}s",
            "values": self.values(from_value, to_value),
            "keyTimes": self.key_times
        })

    def values(self, from_value: str, to_value: str):
        return ';'.join([f"{from_value};{to_value}" for _ in range(self.count)])

    @property
    def key_times(self) -> str:
        return ';'.join(
            [f"{index / self.count};{(index + 1) / self.count}" for index in range(self.count)])
