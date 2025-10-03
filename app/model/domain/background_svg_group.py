from pydantic import BaseModel


class BackgroundSvgGroup(BaseModel):
    @staticmethod
    def build_group(width: float, height: float, color: str) -> str:
        return f"<g><rect width={width} height={height} fill={color} /></g>"