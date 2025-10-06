from shapely import MultiPoint
from shapely.affinity import scale


class GeometryUtil:
    @staticmethod
    def mirror(points: list[tuple[float, float]], x: bool, y: bool) -> list[tuple[float, float]]:
        geom: MultiPoint = MultiPoint(points)
        mirrored = scale(
            geom,
            xfact=-1 if x else 1,
            yfact=-1 if y else 1,
            origin=(0, 0),
        )
        return [(pt.x, pt.y) for pt in mirrored.geoms]
