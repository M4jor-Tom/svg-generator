from pydantic import BaseModel

from model.domain import SvgElement
from util import DomUtil


class BackgroundSvgElement(BaseModel, SvgElement):
    width: float
    height: float
    color: str

    def build(self) -> str:
        return DomUtil.build_element("rect", {"width": f"{self.width}", "height": f"{self.height}", "fill": self.color})
