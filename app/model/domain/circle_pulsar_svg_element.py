from pydantic import BaseModel

from model.domain import SvgElement, PulseMode
from util import DomUtil


class CirclePulsarSvgElement(BaseModel, SvgElement):
    cx: str
    cy: str
    radius: str
    thickness: float
    fill_rgb: tuple[float, float, float, float]
    stroke_rgb: tuple[float, float, float]
    pulse_mode: PulseMode

    def build_circle_pulse_animation(self, radius: str) -> str:
        return self.pulse_mode.build_animation(f"{radius}", "0", "animate", "r")

    def build(self) -> str:
        return DomUtil.build_element(
            "circle", {
                "cx": self.cx, "cy": self.cy,
                "r": self.radius, "stroke-width": f"{self.thickness}",
                "fill": DomUtil.build_str_color(self.fill_rgb),
                "stroke": DomUtil.build_str_color(self.stroke_rgb)},
            dom_content=self.build_circle_pulse_animation(radius=self.radius))
