from math import cos, sin, tau

from pydantic import BaseModel

from model.domain import PulseMode, PolygonSvgGroup
from util import DomUtil


class CircularPolygonSvgGroup(PolygonSvgGroup, BaseModel):
    angles_count: int
    pulse_mode: PulseMode | None

    def build_line_color(self, current_point_index: int, total_lines_count: int) -> \
            tuple[float, float, float]:
        if self.pulse_mode is None:
            return 0, 0, 0
        if not self.progressive_color:
            return self.initial_rgb
        clearest_color_value: int = max(self.initial_rgb)
        progression_margin: int = 255 - clearest_color_value
        location: float = current_point_index / total_lines_count
        rgb_offset: float = location * progression_margin
        return tuple[float, float, float]([color + rgb_offset for color in self.initial_rgb])

    def build_line_content(self, from_rgb: tuple[float, float, float],
                           to_rgb: tuple[float, float, float]) -> str | None:
        if self.pulse_mode is None:
            return None
        return self.pulse_mode.build_animation(
            DomUtil.build_str_color(from_rgb),
            DomUtil.build_str_color(to_rgb),
            "animate", "stroke")

    @staticmethod
    def build_angles(angles_count: int) -> list[tuple[float, float]]:
        points: list[tuple[float, float]] = []
        for i in range(angles_count):
            angle_in_radians: float = -tau / 4 + i * (tau / angles_count)
            x: float = cos(angle_in_radians)
            y: float = sin(angle_in_radians)
            points.append((x, y))
        return points

    def build(self) -> str:
        elements: list[str] = []
        angles: list[tuple[float, float]] = CircularPolygonSvgGroup.build_angles(
            angles_count=self.angles_count)
        for line_element in self.build_lines(points=angles):
            elements.append(line_element)
        return f"<g>{"".join(elements)}</g>"
