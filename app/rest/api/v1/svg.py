from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse

from constant import svg_strip, master
from service import SvgGeneratorService

svg_router: APIRouter = APIRouter()

@svg_router.get(path=svg_strip, tags=[master], response_class=HTMLResponse)
def get_svg(svg_generator_service: SvgGeneratorService = Depends(SvgGeneratorService)) -> str:
    return svg_generator_service.get_svg(width=1500, height=900, indent=False)
