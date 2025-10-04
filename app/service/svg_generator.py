from xml.dom.minidom import Document

from model.domain import PolygonSvgGroup, BackgroundSvgGroup, CirclePulsarSvgGroup
from xml.dom import minidom

from util import DomUtil


class SvgGeneratorService:

    @staticmethod
    def indent_svg(svg: str, indentation_spaces: int) -> str:
        dom: Document = minidom.parseString(svg)
        indented_svg: str = dom.toprettyxml(indent=" " * indentation_spaces)
        return "\n".join(
            [line for line in indented_svg.split("\n") if line.strip()]
        )

    @staticmethod
    def get_svg(width: float, height: float, indent: bool) -> str:
        circle_radius: float = height / 2
        polygon_radius: float = height / 2
        cx: float = height / 2
        cy: float = height / 2
        groups: tuple[str, ...] = (
            BackgroundSvgGroup.build_group(width, height, "white"),
            CirclePulsarSvgGroup(
                radius=circle_radius,
                fill_rgb=(255, 255, 255), stroke_rgb=(0, 0, 127),
                cx=cx, cy=cy, thickness=3
            ).build(),
            PolygonSvgGroup(
                angles_count=7, radius=polygon_radius, thickness=5,
                rgb=(0, 0, 50), progressive_color=True, cx=cx, cy=cy
            ).build()
        )
        groups_with_offset: str = DomUtil.build_element(
            "g", {"transform": f"translate({width / 6}, {0})"}, ''.join(groups))
        unindented_svg: str = (
            f"<svg xmlns='http://www.w3.org/2000/svg' "
            f"width='{width}' height='{height}' "
            f"viewBox='0 0 {width} {height}'>{groups_with_offset}</svg>"
        )
        if indent:
            return SvgGeneratorService.indent_svg(unindented_svg, indentation_spaces=2)
        return unindented_svg
