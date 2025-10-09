from pydantic import BaseModel


class State(BaseModel):
    polygon_angles: int
    pulse_circle: bool
    pulse_polygon: bool
    space_theta_wings: float
    animate_theta_eye: bool
    theta_eye_butterfly_animation: bool
    theta_eye_color: tuple[int, int, int]
    background_color: tuple[int, int, int]
    lines_color: tuple[int, int, int]

    def is_pulsating(self) -> bool:
        return self.pulse_polygon or self.pulse_circle
