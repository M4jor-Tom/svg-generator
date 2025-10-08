from pydantic import BaseModel

from model.domain import AnimationMode


class PulseMode(AnimationMode, BaseModel):

    def values(self, from_value: str, to_value: str):
        return ';'.join([f"{from_value};{to_value}" for _ in range(self.count)])

    @property
    def key_times(self) -> str:
        return ';'.join(
            [f"{index / self.count};{(index + 1) / self.count}" for index in range(self.count)])
