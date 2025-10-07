from fastapi import APIRouter, Depends

from constant.url import control_strip
from model.domain import State
from service import StateService, get_state_service

control_router: APIRouter = APIRouter()

@control_router.post(path=control_strip)
def post_state(state: State = get_state_service().state, state_service: StateService = Depends(get_state_service)) -> None:
    state_service.state = state
