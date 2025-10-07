from fastapi import APIRouter

from constant import ui_strip
from .svg import svg_router

ui_router: APIRouter = APIRouter(prefix=ui_strip)

ui_router.include_router(svg_router)
