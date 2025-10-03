from fastapi import APIRouter

from constant import v1_strip
from .svg import svg_router

v1_router: APIRouter = APIRouter(prefix=v1_strip)

v1_router.include_router(svg_router)
