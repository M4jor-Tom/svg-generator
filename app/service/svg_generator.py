from xml.dom.minidom import Document

from model.domain import PolygonSvgGroup, BackgroundSvgGroup
from xml.dom import minidom


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
        groups: tuple[str, ...] = (
            BackgroundSvgGroup.build_group(width, height, "white"),
            PolygonSvgGroup(
                angles_count=5, radius=height / 2, thickness=1.5, circle_visible=False, offset_x=width / 6, offset_y=0,
                rgb=(0, 0, 50), progressive_color=True
            ).build()
        )
        unindented_svg: str = (
            f"<svg xmlns='http://www.w3.org/2000/svg' "
            f"width='{width}' height='{height}' "
            f"viewBox='0 0 {width} {height}'>{''.join(groups)}</svg>"
        )
        if indent:
            return SvgGeneratorService.indent_svg(unindented_svg, indentation_spaces=2)
        return unindented_svg
