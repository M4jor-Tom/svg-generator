from pydantic import BaseModel

from model.domain import PolygonSvgGroup
from util import DomUtil, GeometryUtil


class ThetaSvgGroup(PolygonSvgGroup, BaseModel):

    def build_line_color(self, current_point_index: int, total_lines_count: int) -> \
            tuple[float, float, float]:
        return 0, 0, 0

    def build_line_content(self, from_rgb: tuple[float, float, float],
                           to_rgb: tuple[float, float, float]) -> str | None:
        return ""

    @staticmethod
    def normalize_coordinate_to_vmin(coordinate: float) -> str:
        return f"{((coordinate + 1) / 2) * 100}vmin"

    @staticmethod
    def build_right_bottom_part_points() -> list[tuple[float, float]]:
        return [(0, .05), (0, .2), (.1, -.05)]

    @staticmethod
    def build_left_bottom_part_points() -> list[tuple[float, float]]:
        return GeometryUtil.mirror(ThetaSvgGroup.build_right_bottom_part_points(), x=True, y=False)

    @staticmethod
    def build_left_top_part_points() -> list[tuple[float, float]]:
        return GeometryUtil.mirror(ThetaSvgGroup.build_right_bottom_part_points(), x=True, y=True)

    @staticmethod
    def build_right_top_part_points() -> list[tuple[float, float]]:
        return GeometryUtil.mirror(ThetaSvgGroup.build_right_bottom_part_points(), x=False, y=True)

    @staticmethod
    def build_eye(animate: bool) -> str:
        eye_color: str = DomUtil.build_str_color((255, 0, 0))
        transparent: str = DomUtil.build_str_color((0, 0, 0, 0))
        centered_attributes: dict[str, str] = {"cy": "50vmin", "cx": "50vmin"}
        return ''.join([
            DomUtil.build_element(
                "circle", {**centered_attributes, "r": ".3vmin", "fill": eye_color}),
            DomUtil.build_element(
                "circle", {**centered_attributes, "r": ".6vmin", "fill": transparent, "stroke": eye_color}
            )
        ])

    def build(self) -> str:
        return DomUtil.build_element("g", {}, ''.join([
            ''.join(self.build_lines(ThetaSvgGroup.build_left_bottom_part_points())),
            ''.join(self.build_lines(ThetaSvgGroup.build_right_bottom_part_points())),
            ''.join(self.build_lines(ThetaSvgGroup.build_left_top_part_points())),
            ''.join(self.build_lines(ThetaSvgGroup.build_right_top_part_points())),
            ThetaSvgGroup.build_eye(animate=False)
        ]))
