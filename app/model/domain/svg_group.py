from abc import ABC, abstractmethod


class SvgGroup(ABC):
    @abstractmethod
    def build(self) -> str:
        pass
