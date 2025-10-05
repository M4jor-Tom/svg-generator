from abc import ABC, abstractmethod


class SvgElement(ABC):

    @abstractmethod
    def build(self) -> str:
        pass
