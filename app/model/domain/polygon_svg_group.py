from math import cos, sin, tau

from pydantic import BaseModel

from model.domain import SvgElement
from util import DomUtil


class PolygonSvgGroup(BaseModel, SvgElement):
    angles_count: int
    thickness: float
    rgb: tuple[int, int, int]
    progressive_color: bool
    pulse: bool

    def build_polygon_pulse_animation(self, duration_s: float) -> str:
        return DomUtil.build_element("animateTransform", {
            "attributeName": "transform",
            "type": "rotate",
            "fill": "freeze",
            "dur": f"{duration_s}s",
            "from": f"0 {self.cx} {self.cy}",
            "to": f"{360} {self.cx} {self.cy}"
        })

    @staticmethod
    def build_angles(angles_count: int) -> list[tuple[float, float]]:
        points: list[tuple[float, float]] = []
        for i in range(angles_count):
            angle_in_radians: float = -tau / 4 + i * (tau / angles_count)
            x: float = cos(angle_in_radians)
            y: float = sin(angle_in_radians)
            points.append((x, y))
        return points

    @staticmethod
    def normalize_coordinate_to_percent(coordinate: float) -> str:
        return f"{((coordinate + 1) / 2) * 100}vmin"

    @staticmethod
    def build_lines(angles: list[tuple[float, float]], thickness: float, initial_rgb: tuple[int, int, int],
                    progressive_color: bool) -> list[str]:
        angles_count: int = len(angles)
        lines_total_count: int = PolygonSvgGroup.compute_lines_amount(angles_count=angles_count)
        lines_elements: list[str] = []
        current_angle_index: int = 0
        for angle_index in range(angles_count):
            x1, y1 = map(PolygonSvgGroup.normalize_coordinate_to_percent, angles[angle_index])
            for j in range(angle_index + 1, angles_count):
                x2, y2 = map(PolygonSvgGroup.normalize_coordinate_to_percent, angles[j])
                color: str = PolygonSvgGroup.build_progressive_line_color(
                    index=current_angle_index, total_amount=lines_total_count, initial_rgb=initial_rgb) \
                    if progressive_color \
                    else DomUtil.build_str_color(initial_rgb)
                lines_elements.append(
                    DomUtil.build_element("line", {"x1": x1, "y1": y1,
                                                   "x2": x2, "y2": y2,
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

        if self.pulse:
            elements.append(self.build_polygon_pulse_animation(duration_s=1))

        angles: list[tuple[float, float]] = PolygonSvgGroup.build_angles(
            angles_count=self.angles_count)
        for line_element in PolygonSvgGroup.build_lines(
                angles=angles,
                initial_rgb=self.rgb, progressive_color=self.progressive_color, thickness=self.thickness):
            elements.append(line_element)

        return f"<g>{"".join(elements)}</g>"
