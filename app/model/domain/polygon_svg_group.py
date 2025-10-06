from abc import ABC, abstractmethod

from pydantic import BaseModel
from itertools import combinations

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
    def build_line_color(self, current_point_index: int, total_lines_count: int) -> tuple[float, float, float]:
        pass

    @abstractmethod
    def build_line_content(self, from_rgb: tuple[float, float, float],
                           to_rgb: tuple[float, float, float]) -> str | None:
        pass

    def build_lines(self, points: list[tuple[float, float]]) -> list[str]:
        current_point_index: int = 0
        lines_total_count: int = PolygonSvgGroup.compute_lines_amount(angles_count=len(points))
        lines_elements: list[str] = []
        line_combinations = combinations(points, 2)
        for point1, point2 in line_combinations:
            x1, y1 = map(PolygonSvgGroup.normalize_coordinate_to_vmin, point1)
            x2, y2 = map(PolygonSvgGroup.normalize_coordinate_to_vmin, point2)
            color: tuple[float, float, float] = self.build_line_color(current_point_index, lines_total_count)
            lines_elements.append(DomUtil.build_element("line", {
                "x1": f"{x1}", "y1": f"{y1}",
                "x2": f"{x2}", "y2": f"{y2}",
                "stroke-width": f"{self.thickness}",
                "stroke": DomUtil.build_str_color(color)
            }, self.build_line_content(color, (0, 0, 0))))
            current_point_index += 1
        return lines_elements
