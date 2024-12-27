from typing import Tuple, Optional

class Landmark:
    def __init__(self, x, y, z, visibility, name=Optional[None]):
        self.x = x
        self.y = y
        self.z = z
        self.visibility = visibility
        self.name = name

    def __str__(self):
        return f"Landmark '{self.name}': (x={self.x}, y={self.y}, z={self.z}, visibility={self.visibility})"

    def normalized_coordinates(self)->Tuple[float, float]:
        return self.x, self.y

    def pixel_coordinates(self, width: int, height: int)->Tuple[int, int]:
        a = np.array(self.normalized_coordinates())
        b = np.array((width, height))
        return tuple(np.multiply(a, b).astype(int))

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "visibility": self.visibility,
            "name": self.name
        }