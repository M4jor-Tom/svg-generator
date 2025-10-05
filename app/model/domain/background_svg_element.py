from pydantic import BaseModel

from model.domain import SvgElement
from util import DomUtil


class BackgroundSvgElement(BaseModel, SvgElement):
    width: str
    height: str
    rgb: tuple[float, float, float]

    def build(self) -> str:
        return DomUtil.build_element(
            "rect",
            {"width": self.width, "height": self.height, "fill": DomUtil.build_str_color(self.rgb)})
