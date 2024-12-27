from typing import Optional, Tuple
from .landmark import Landmark

class BodySegment:

    def __init__(self, start_landmark: Landmark, end_landmark: Landmark, name=Optional[None]):
        self.start_landmark = start_landmark
        self.end_landmark = end_landmark
        self.name = name

    def normalized_vector(self)->Tuple[float, float]:
        a = np.array(self.start_landmark.normalized_coordinates())
        b = np.array(self.end_landmark.normalized_coordinates())
        return tuple(b - a)

    def pixel_vector(self, width: int, height: int)->Tuple[int, int]:
        a = np.array(self.start_landmark.pixel_coordinates(width, height))
        b = np.array(self.end_landmark.pixel_coordinates(width, height))
        return tuple(b - a)

    def lenght(self)->float:
        return np.linalg.norm(self.normalized_vector())

    def pixel_lenght(self, width: int, height: int)->float:
        return np.linalg.norm(self.pixel_vector(width, height))

    def direction(self)->Tuple[float, float]:
        return self.normalized_vector() / self.lenght() if self.lenght() > 0 else (0.0, 0.0)

    @property
    def _calculate_angle(a: Tuple[float, float], b: Tuple[float, float])->int:
        a = np.array(a)
        b = np.array(b)
        angle_radians = np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        angle_degrees = np.degrees(angle_radians)
        if angle_degrees < 0:
            angle_degrees = 360 + angle_degrees
        elif angle_degrees > 180:
            angle_degrees = 360 - angle_degrees
        return angle_degrees

    def vertical_axis_angle(self)->int:
        return self._calculate_angle(self.normalized_vector(), (0.0, 1.0))

    def horizontal_axis_angle(self)->int:
        return self._calculate_angle(self.normalized_vector(), (1.0, 0.0))

    def angle_between(self, other)->int:
        return self._calculate_angle(self.normalized_vector(), other.normalized_vector())

    def __str__(self):
        return f"BodySegment '{self.name}': {self.start_landmark} -> {self.end_landmark}"

    def to_dict(self):
        return {
            "start_landmark": self.start_landmark.to_dict(),
            "end_landmark": self.end_landmark.to_dict(),
            "name": self.name
        }