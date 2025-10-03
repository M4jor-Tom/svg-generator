from math import cos, sin, tau

from pydantic import BaseModel


class PolygonSvgGroup(BaseModel):
    @staticmethod
    def escape_attribute(string: str) -> str:
        return (
            string.replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    @staticmethod
    def build_attributes_from_dict(attributes: dict[str, str]) -> str:
        return " ".join(f'{key}="{PolygonSvgGroup.escape_attribute(value)}"' for key, value in attributes.items())

    @staticmethod
    def build_circle(cx: float, cy: float, radius: float, thickness: float, color: str) -> str:
        circle_attributes: dict[str, str] = {"cx": f"{cx}", "cy": f"{cy}", "r": f"{radius}", "stroke": color, "stroke-width": f"{thickness}"}
        return f"<circle {PolygonSvgGroup.build_attributes_from_dict(circle_attributes)}/>"

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
    def build_lines(angles: list[tuple[float, float]], thickness: float, color: str) -> list[str]:
        attributes: dict[str, str] = {"stroke": color, "stroke-width": f"{thickness}"}
        angles_count: int = len(angles)
        lines_elements: list[str] = []
        for angle_index in range(angles_count):
            x1, y1 = angles[angle_index]
            for j in range(angle_index + 1, angles_count):
                x2, y2 = angles[j]
                lines_elements.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {PolygonSvgGroup.build_attributes_from_dict(attributes)} />'
                )
        return lines_elements

    @staticmethod
    def build_group(
            angles_count: int,
            radius: float,
            thickness: float,
            circle_visible: bool,
            init_red: float,
            init_green: float,
            init_blue: float,
            offset_x: float,
            offset_y: float
    ) -> str:
        elements: list[str] = []
        cx: float = radius
        cy: float = radius
        color: str = "white"

        if angles_count < 2:
            raise ValueError("n must be >= 2")

        if circle_visible:
            elements.append(PolygonSvgGroup.build_circle(cx=cx, cy=cy, radius=radius, color=color, thickness=thickness))

        angles: list[tuple[float, float]] = PolygonSvgGroup.build_angles(angles_count=angles_count, cx=cx, cy=cy, radius=radius)
        for line_element in PolygonSvgGroup.build_lines(angles=angles, color=color, thickness=thickness):
            elements.append(line_element)

        return f"<g transform='translate({offset_x}, {offset_y})'>{"".join(elements)}</g>"
