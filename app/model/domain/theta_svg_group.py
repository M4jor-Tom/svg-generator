from pydantic import BaseModel

from model.domain import PolygonSvgGroup
from model.domain.butterfly_mode import ButterflyMode
from util import DomUtil, GeometryUtil


class ThetaSvgGroup(PolygonSvgGroup, BaseModel):
    animate: bool
    spacing: float
    butterfly_mode: ButterflyMode | None
    eye_color: tuple[int, int, int]

    def build_line_color(self, current_point_index: int, total_lines_count: int) -> \
            tuple[float, float, float]:
        return self.initial_rgb

    def build_line_content(self, from_rgb: tuple[float, float, float],
                           to_rgb: tuple[float, float, float]) -> str | None:
        return ""

    @staticmethod
    def normalize_coordinate(coordinate: float) -> str:
        return f"{((coordinate + 1) / 2) * 100}"

    def build_right_bottom_part_points(self) -> list[tuple[float, float]]:
        return [(self.spacing, .05), (self.spacing, .2), (.1 + self.spacing, -.05)]

    def build_left_bottom_part_points(self) -> list[tuple[float, float]]:
        return GeometryUtil.mirror(self.build_right_bottom_part_points(), x=True, y=False)

    def build_left_top_part_points(self) -> list[tuple[float, float]]:
        return GeometryUtil.mirror(self.build_right_bottom_part_points(), x=True, y=True)

    def build_right_top_part_points(self) -> list[tuple[float, float]]:
        return GeometryUtil.mirror(self.build_right_bottom_part_points(), x=False, y=True)

    def build_eye_animation(self) -> str:
        return DomUtil.build_element("animateTransform",
                                     {"type": "rotate", "attributeName": "transform", "from": "0 50 50",
                                      "to": "360 50 50",
                                      "dur": "2.5s", "repeatCount": "indefinite"}) \
            if self.butterfly_mode is None \
            else self.butterfly_mode.build_animation(from_value=".5", to_value="1", animation_tag="animate",
                                                     animated_property="stroke-dasharray")

    def build_eye(self) -> str:
        eye_color: str = DomUtil.build_str_color(self.eye_color)
        transparent: str = DomUtil.build_str_color((0, 0, 0, 0))
        common_attributes: dict[str, str] = {"cy": "50", "cx": "50", "stroke-width": '.2'}
        eye_center: str = DomUtil.build_element(
            "circle", {**common_attributes, "r": ".3", "fill": eye_color})
        eye_static_contour: str = DomUtil.build_element(
            "circle", {**common_attributes, "r": ".6", "fill": transparent, "stroke": eye_color}
        )
        eye_animated_contour: str = DomUtil.build_element(
            "circle",
            {**common_attributes, "r": ".8", "fill": transparent, "stroke": eye_color, "stroke-dasharray": ".5"},
            self.build_eye_animation()
        )
        return ''.join([eye_center, eye_animated_contour]) if self.animate else ''.join(
            [eye_center, eye_static_contour])

    def build(self) -> str:
        return DomUtil.build_element("g", {}, ''.join([
            ''.join(self.build_lines(self.build_left_bottom_part_points())),
            ''.join(self.build_lines(self.build_right_bottom_part_points())),
            ''.join(self.build_lines(self.build_left_top_part_points())),
            ''.join(self.build_lines(self.build_right_top_part_points())),
            self.build_eye()
        ]))
