from math import cos, sin, tau

from pydantic import BaseModel

from model.domain import SvgElement, PulseMode
from util import DomUtil


class PolygonSvgGroup(BaseModel, SvgElement):
    angles_count: int
    thickness: float
    rgb: tuple[int, int, int]
    progressive_color: bool
    pulse_mode: PulseMode | None

    @staticmethod
    def build_line_pulse_animation(pulse_mode: PulseMode, from_rgb: tuple[float, float, float],
                                   to_rgb: tuple[float, float, float]) -> str:
        return pulse_mode.build_animation(
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

    @staticmethod
    def normalize_coordinate_to_percent(coordinate: float) -> str:
        return f"{((coordinate + 1) / 2) * 100}vmin"

    def build_lines(self, angles: list[tuple[float, float]], thickness: float, initial_rgb: tuple[int, int, int],
                    progressive_color: bool) -> list[str]:
        angles_count: int = len(angles)
        lines_total_count: int = PolygonSvgGroup.compute_lines_amount(angles_count=angles_count)
        lines_elements: list[str] = []
        current_angle_index: int = 0
        for angle_index in range(angles_count):
            x1, y1 = map(PolygonSvgGroup.normalize_coordinate_to_percent, angles[angle_index])
            for j in range(angle_index + 1, angles_count):
                x2, y2 = map(PolygonSvgGroup.normalize_coordinate_to_percent, angles[j])
                color: tuple[float, float, float] = PolygonSvgGroup.build_progressive_line_color(
                    index=current_angle_index, total_amount=lines_total_count, initial_rgb=initial_rgb) \
                    if progressive_color \
                    else initial_rgb
                lines_elements.append(
                    DomUtil.build_element(
                        "line", {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke-width": f"{thickness}", "stroke": DomUtil.build_str_color(color)},
                        PolygonSvgGroup.build_line_pulse_animation(
                            pulse_mode=self.pulse_mode, from_rgb=color, to_rgb=(0, 0, 0))
                        if self.pulse_mode is not None else None)
                )
                current_angle_index += 1
        return lines_elements

    @staticmethod
    def compute_lines_amount(angles_count: int) -> int:
        return int(angles_count * (angles_count - 1) / 2)

    @staticmethod
    def build_progressive_line_color(index: int, total_amount: int, initial_rgb: tuple[int, int, int]) -> tuple[
        float, float, float]:
        clearest_color_value: int = max(initial_rgb)
        progression_margin: int = 255 - clearest_color_value
        location: float = index / total_amount
        rgb_offset: float = location * progression_margin
        return tuple[float, float, float]([color + rgb_offset for color in initial_rgb])

    def build(self) -> str:
        elements: list[str] = []

        angles: list[tuple[float, float]] = PolygonSvgGroup.build_angles(
            angles_count=self.angles_count)
        for line_element in self.build_lines(
                angles=angles,
                initial_rgb=self.rgb, progressive_color=self.progressive_color, thickness=self.thickness):
            elements.append(line_element)

        return f"<g>{"".join(elements)}</g>"
