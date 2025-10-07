from pydantic import BaseModel


class State(BaseModel):
    polygon_angles: int
    pulse_circle: bool
    pulse_polygon: bool
    space_theta_wings: float
    animate_theta_eye: bool
