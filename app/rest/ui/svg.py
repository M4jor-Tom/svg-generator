from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse

from constant import svg_strip, master
from service import SvgGeneratorService, get_svg_generator_service, StateService, get_state_service
from util import DomUtil

svg_router: APIRouter = APIRouter()


@svg_router.get(path=svg_strip, tags=[master], response_class=HTMLResponse)
def get_web_svg(
        state_service: StateService = Depends(get_state_service),
        svg_generator_service: SvgGeneratorService = Depends(get_svg_generator_service)
) -> str:
    background_rgb: tuple[float, float, float] = state_service.state.background_color
    return DomUtil.wrap_with_html(
        svg_generator_service.build_svg(indent=False, background_rgb=None), reload_delay_s=5,
        background_rgb=background_rgb)
