from abc import ABC, abstractmethod

from pydantic import BaseModel

from model.domain import SvgElement
from util import DomUtil


class PolygonSvgGroup(SvgElement, BaseModel, ABC):
    thickness: float
    initial_rgb: tuple[int, int, int]
    progressive_color: bool

    @staticmethod
    def compute_lines_amount(angles_count: int) -> int:
        return int(angles_count * (angles_count - 1) / 2)

    @staticmethod
    def normalize_coordinate_to_vmin(coordinate: float) -> str:
        return f"{((coordinate + 1) / 2) * 100}vmin"

    @abstractmethod
    def build_line_color(
            self, current_point_index: int, total_lines_count: int,
            initial_color: tuple[int, int, int]) -> tuple[float, float, float]:
        pass

    @abstractmethod
    def build_line_content(self, line_color: tuple[float, float, float]) -> str | None:
        pass

    def build_lines(self, points: list[tuple[float, float]]) -> list[str]:
        points_count: int = len(points)
        lines_total_count: int = PolygonSvgGroup.compute_lines_amount(angles_count=points_count)
        lines_elements: list[str] = []
        current_point_index: int = 0
        for point_index in range(points_count):
            x1, y1 = map(PolygonSvgGroup.normalize_coordinate_to_vmin, points[point_index])
            for j in range(point_index + 1, points_count):
                x2, y2 = map(PolygonSvgGroup.normalize_coordinate_to_vmin, points[j])
                color: tuple[float, float, float] = self.build_line_color(
                    current_point_index, lines_total_count, self.initial_rgb) \
                    if self.progressive_color else self.initial_rgb
                lines_elements.append(
                    DomUtil.build_element(
                        "line", {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke-width": f"{self.thickness}",
                                 "stroke": DomUtil.build_str_color(color)}, self.build_line_content(color))
                )
                current_point_index += 1
        return lines_elements

