from math import cos, sin, tau

from pydantic import BaseModel

from model.domain import SvgGroup
from util import DomUtil


class PolygonSvgGroup(BaseModel, SvgGroup):
    angles_count: int
    radius: float
    thickness: float
    rgb: tuple[int, int, int]
    progressive_color: bool
    cx: float
    cy: float

    @staticmethod
    def build_polygon_pulse_animation(radius: float) -> str:
        return DomUtil.build_element("animateTransform", {
            "attributeName": "transform",
            "type": "rotate",
            "fill": "freeze",
            "dur": "1s",
            "values": f"{radius};0;{radius};0;{radius};0",
            "keyTimes": "0;0.3333;0.3333;0.6667;0.6667;1"
        })

    @staticmethod
    def build_angles(angles_count: int, cx: float, cy: float, radius: float) -> list[tuple[float, float]]:
        points: list[tuple[float, float]] = []
        for i in range(angles_count):
            angle_in_radians: float = -tau / 4 + i * (tau / angles_count)
            x: float = cx + radius * cos(angle_in_radians)
            y: float = cy + radius * sin(angle_in_radians)
            points.append((x, y))
        return points

    @staticmethod
    def build_lines(angles: list[tuple[float, float]], thickness: float, initial_rgb: tuple[int, int, int],
                    progressive_color: bool) -> list[str]:
        angles_count: int = len(angles)
        lines_total_count: int = PolygonSvgGroup.compute_lines_amount(angles_count=angles_count)
        lines_elements: list[str] = []
        current_angle_index: int = 0
        for angle_index in range(angles_count):
            x1, y1 = angles[angle_index]
            for j in range(angle_index + 1, angles_count):
                x2, y2 = angles[j]
                color: str = PolygonSvgGroup.build_progressive_line_color(
                    index=current_angle_index, total_amount=lines_total_count, initial_rgb=initial_rgb) \
                    if progressive_color \
                    else DomUtil.build_str_color(initial_rgb)
                lines_elements.append(
                    DomUtil.build_element("line", {"x1": f"{x1}", "y1": f"{y1}",
                                                   "x2": f"{x2}", "y2": f"{y2}",
                                                   "stroke": color, "stroke-width": f"{thickness}"})
                )
                current_angle_index += 1
        return lines_elements

    @staticmethod
    def compute_lines_amount(angles_count: int) -> int:
        return int(angles_count * (angles_count - 1) / 2)

    @staticmethod
    def build_progressive_line_color(index: int, total_amount: int, initial_rgb: tuple[int, int, int]) -> str:
        clearest_color_value: int = max(initial_rgb)
        progression_margin: int = 255 - clearest_color_value
        location: float = index / total_amount
        rgb_offset: float = location * progression_margin
        return DomUtil.build_str_color(
            tuple[float, float, float]([color + rgb_offset for color in initial_rgb]))

    def build(self) -> str:
        elements: list[str] = []

        angles: list[tuple[float, float]] = PolygonSvgGroup.build_angles(
            angles_count=self.angles_count, cx=self.cx, cy=self.cy, radius=self.radius)
        for line_element in PolygonSvgGroup.build_lines(
                angles=angles,
                initial_rgb=self.rgb, progressive_color=self.progressive_color, thickness=self.thickness):
            elements.append(line_element)

        return f"<g>{"".join(elements)}</g>"
