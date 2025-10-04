from pydantic import BaseModel

from model.domain import SvgGroup
from util import DomUtil


class CirclePulsarSvgGroup(BaseModel, SvgGroup):
    cx: float
    cy: float
    radius: float
    thickness: float
    fill_rgb: tuple[float, float, float]
    stroke_rgb: tuple[float, float, float]

    @staticmethod
    def build_circle_pulse_animation(radius: float) -> str:
        return DomUtil.build_element("animate", {
            "attributeName": "r",
            "fill": "freeze",
            "dur": "1s",
            "values": f"{radius};0;{radius};0;{radius};0",
            "keyTimes": "0;0.3333;0.3333;0.6667;0.6667;1"
        })

    def build(self) -> str:
        return DomUtil.build_element("circle", {
            "cx": f"{self.cx}", "cy": f"{self.cy}",
            "r": f"{self.radius}", "stroke-width": f"{self.thickness}", "fill": DomUtil.build_str_color(self.fill_rgb),
            "stroke": DomUtil.build_str_color(self.stroke_rgb)},
                                     dom_content=CirclePulsarSvgGroup.build_circle_pulse_animation(radius=self.radius))
