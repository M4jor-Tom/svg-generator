from pydantic import BaseModel

from model.domain import AnimationMode


class ButterflyMode(AnimationMode, BaseModel):

    def values(self, from_value: str, to_value: str):
        return ';'.join([f"{from_value};{to_value};{to_value};{from_value}" for _ in range(self.count)])

    @property
    def key_times(self) -> str:
        butterfly_count: int = self.count * 2
        return ';'.join(
            [f"{index / butterfly_count};{(index + 1) / butterfly_count}" for index in range(butterfly_count)])
