from abc import ABC, abstractmethod

from pydantic import BaseModel

from util import DomUtil


class AnimationMode(BaseModel, ABC):
    duration_s: float
    count: int
    repeat: bool

    def build_animation(self, from_value: str, to_value: str, animation_tag: str, animated_property: str) -> str:
        return DomUtil.build_element(animation_tag, {
            **self.get_repeat_or_freeze_dict(),
            "attributeName": animated_property,
            "dur": f"{self.duration_s}s",
            "values": self.values(from_value, to_value),
            "keyTimes": self.key_times
        })

    def get_repeat_or_freeze_dict(self) -> dict[str, str]:
        return {"repeatCount": "indefinite"} if self.repeat else {"fill": "freeze"}

    @abstractmethod
    def values(self, from_value: str, to_value: str):
        pass

    @property
    @abstractmethod
    def key_times(self) -> str:
        pass
