from .state_service import StateService
from .svg_generator_service import SvgGeneratorService

state_service: StateService = StateService()
svg_generator_service: SvgGeneratorService = SvgGeneratorService(state_service=state_service)

def get_state_service() -> StateService:
    return state_service

def get_svg_generator_service() -> SvgGeneratorService:
    return svg_generator_service
