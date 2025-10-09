from model.domain import State


class StateService:
    _state: State
    _state_was_set_since_last_reaction: bool

    def __init__(self):
        self._state = State(
            pulse_polygon=False,
            pulse_circle=False,
            polygon_angles=7,
            animate_theta_eye=False,
            theta_eye_butterfly_animation=False,
            space_theta_wings=False,
            lines_color=(0, 0, 0),
            background_color=(220, 220, 220),
            theta_eye_color=(255, 0, 0)
        )
        self._state_was_set_since_last_reaction = False

    def set_state(self, state: State) -> None:
        self._state = state
        self._state_was_set_since_last_reaction = True

    def must_react(self) -> bool:
        result: bool = self._state_was_set_since_last_reaction
        self._state_was_set_since_last_reaction = False
        return result

    def get_state(self) -> State:
        return self._state
