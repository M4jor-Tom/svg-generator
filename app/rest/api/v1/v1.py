from fastapi import APIRouter

from .control import control_router
from constant import v1_strip

v1_router: APIRouter = APIRouter(prefix=v1_strip)

v1_router.include_router(control_router)
