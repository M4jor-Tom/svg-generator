from xml.dom import minidom
from xml.dom.minidom import Document

from model.domain import CircularPolygonSvgGroup, CirclePulsarSvgElement, BackgroundSvgElement, PulseMode, \
    ThetaSvgGroup, ButterflyMode
from service import StateService
from util import DomUtil


class SvgGeneratorService:

    def __init__(self, state_service: StateService):
        self.state_service = state_service

    @staticmethod
    def indent_svg(svg: str, indentation_spaces: int) -> str:
        dom: Document = minidom.parseString(svg)
        indented_svg: str = dom.toprettyxml(indent=" " * indentation_spaces)
        return "\n".join(
            [line for line in indented_svg.split("\n") if line.strip()]
        )

    def build_svg(self, indent: bool, background_rgb: tuple[float, float, float] | None) -> str:
        height: str = "100vmin"
        width: str = "100vmin"
        circle_radius: str = "50"
        cx: str = "50"
        cy: str = "50"
        thickness: float = .4
        pulse_mode: PulseMode = PulseMode(duration_s=1, count=3, repeat=False)
        butterfly_mode: ButterflyMode = ButterflyMode(duration_s=5, count=1, repeat=False)
        background_svg: BackgroundSvgElement | None = BackgroundSvgElement(
            width=width, height=height, rgb=background_rgb) if background_rgb else None
        circle_pulsar: CirclePulsarSvgElement = CirclePulsarSvgElement(
            radius=circle_radius, pulse_mode=pulse_mode,
            fill_rgb=(255, 255, 255, 0), stroke_rgb=(0, 0, 127),
            cx=cx, cy=cy, thickness=thickness
        )
        circular_polygon_svg_group: CircularPolygonSvgGroup = CircularPolygonSvgGroup(
            angles_count=self.state_service.state.polygon_angles, thickness=thickness, initial_rgb=(0, 0, 50),
            progressive_color=True,
            pulse_mode=pulse_mode if self.state_service.state.pulse_polygon else None)
        theta_svg_group: ThetaSvgGroup = ThetaSvgGroup(
            initial_rgb=(0, 0, 0), thickness=thickness, progressive_color=False,
            spacing=self.state_service.state.space_theta_wings,
            animate=self.state_service.state.animate_theta_eye,
            butterfly_mode=butterfly_mode if self.state_service.state.theta_eye_butterfly_animation else None)
        groups: list[str] = []
        if background_svg is not None:
            groups.append(background_svg.build())
        if self.state_service.state.pulse_circle:
            groups.append(circle_pulsar.build())
        groups.append(circular_polygon_svg_group.build())
        groups.append(theta_svg_group.build())

        unindented_svg: str = DomUtil.build_element(
            "svg",
            {
                "xmlns": 'http://www.w3.org/2000/svg',
                "width": f"{width}", "height": f"{height}",
                "viewBox": f'0 0 100 100'
            },
            ''.join(groups)
        )
        if indent:
            return SvgGeneratorService.indent_svg(unindented_svg, indentation_spaces=2)
        return unindented_svg
