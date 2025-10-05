from xml.dom import minidom
from xml.dom.minidom import Document

from model.domain import CircularPolygonSvgGroup, CirclePulsarSvgElement, BackgroundSvgElement, PulseMode
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
    def build_svg(indent: bool, background_rgb: tuple[float, float, float] | None) -> str:
        height: str = "100vmin"
        width: str = "100vmin"
        circle_radius: str = "50vmin"
        cx: str = "50vmin"
        cy: str = "50vmin"
        pulse_mode: PulseMode = PulseMode(duration_s=1, count=3)
        background_svg: BackgroundSvgElement | None = BackgroundSvgElement(
            width=width, height=height, rgb=background_rgb) if background_rgb else None
        circle_pulsar: CirclePulsarSvgElement = CirclePulsarSvgElement(
            radius=circle_radius, pulse_mode=pulse_mode,
            fill_rgb=(255, 255, 255, 0), stroke_rgb=(0, 0, 127),
            cx=cx, cy=cy, thickness=3
        )
        circular_polygon_svg_group: CircularPolygonSvgGroup = CircularPolygonSvgGroup(
            angles_count=7, thickness=5, initial_rgb=(0, 0, 50), progressive_color=True, pulse_mode=pulse_mode)
        groups: tuple[str, ...] = (
            background_svg.build(),
            circle_pulsar.build(),
            circular_polygon_svg_group.build()
        ) if background_svg else (
            circle_pulsar.build(),
            circular_polygon_svg_group.build()
        )
        unindented_svg: str = DomUtil.build_element(
            "svg",
            {
                "xmlns": 'http://www.w3.org/2000/svg',
                "width": f"{width}", "height": f"{height}",
                "viewBox": f'0 0 {height} {height}'
            },
            ''.join(groups)
        )
        if indent:
            return SvgGeneratorService.indent_svg(unindented_svg, indentation_spaces=2)
        return unindented_svg
