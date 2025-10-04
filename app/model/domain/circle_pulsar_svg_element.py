from pydantic import BaseModel

from model.domain import SvgElement
from util import DomUtil


class CirclePulsarSvgElement(BaseModel, SvgElement):
    cx: float
    cy: float
    radius: float
    thickness: float
    fill_rgb: tuple[float, float, float]
    stroke_rgb: tuple[float, float, float]
    pulses_count: int

    @staticmethod
    def build_circle_pulse_animation(radius: float, pulses_count: int, duration_s: float) -> str:
        return DomUtil.build_element("animate", {
            "attributeName": "r",
            "fill": "freeze",
            "dur": f"{duration_s}s",
            "values": ';'.join([f"{radius};0" for _ in range(pulses_count)]),
            "keyTimes": ';'.join(
                [f"{index / pulses_count};{(index + 1) / pulses_count}" for index in range(pulses_count)])
        })

    def build(self) -> str:
        return DomUtil.build_element(
            "circle", {
                "cx": f"{self.cx}", "cy": f"{self.cy}",
                "r": f"{self.radius}", "stroke-width": f"{self.thickness}",
                "fill": DomUtil.build_str_color(self.fill_rgb),
                "stroke": DomUtil.build_str_color(self.stroke_rgb)},
            dom_content=CirclePulsarSvgElement.build_circle_pulse_animation(radius=self.radius,
                                                                            pulses_count=self.pulses_count,
                                                                            duration_s=1))
