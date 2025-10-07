from model.domain import State


class StateService:
    def __init__(self):
        self.state = State(
            pulse_polygon=False,
            pulse_circle=False,
            polygon_angles=7,
            animate_theta_eye=False,
            space_theta_wings=False
        )
