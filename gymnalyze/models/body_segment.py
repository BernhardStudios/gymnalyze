import numpy as np
import cv2
from typing import Optional, Tuple
from .landmark import Landmark
from ..utils import get_point_on_ellipse

class BodySegment:

    def __init__(self, start_landmark: Landmark, end_landmark: Landmark, name=Optional[None]):
        self.start_landmark = start_landmark
        self.end_landmark = end_landmark
        self.name = name

        # check both landmarks have the same image shape
        if self.start_landmark.width != self.end_landmark.width or self.start_landmark.height != self.end_landmark.height:
            raise ValueError("Both landmarks should have the same image shape")

        self.width = self.start_landmark.width
        self.height = self.start_landmark.height

    def normalized_vector(self)->Tuple[float, float]:
        a = np.array(self.start_landmark.normalized_coordinates())
        b = np.array(self.end_landmark.normalized_coordinates())
        return tuple(b - a)

    def pixel_vector(self, width: Optional[int]=None, height: Optional[int]=None)->Tuple[int, int]:
        a = np.array(self.start_landmark.pixel_coordinates(width, height))
        b = np.array(self.end_landmark.pixel_coordinates(width, height))
        return tuple(b - a)

    def lenght(self)->float:
        return np.linalg.norm(self.normalized_vector())

    def pixel_lenght(self, width: Optional[int]=None, height: Optional[int]=None)->float:
        return np.linalg.norm(self.pixel_vector(width, height))

    def direction(self)->Tuple[float, float]:
        return self.normalized_vector() / self.lenght() if self.lenght() > 0 else (0.0, 0.0)

    RADIUS = 50 # Radius of the circle in pixels
    AXIS_RADIUS_RATIO = 1.5

    def vertical_body_segment(self, img_height: Optional[int]=None):
        height = (self.AXIS_RADIUS_RATIO * self.RADIUS / img_height) if img_height else 0.5
        pos = self.start_landmark.normalized_coordinates()
        vertical_axis = BodySegment(
            # start_landmark=Landmark(pos[0], pos[1] - height, 0, 1.0),
            start_landmark=Landmark(pos[0], pos[1], 0, 1.0),
            end_landmark=Landmark(pos[0], pos[1] + height, 0, 1.0)
        )
        return vertical_axis

    def horizontal_body_segment(self, img_width: Optional[int]=None):
        width = (self.AXIS_RADIUS_RATIO * self.RADIUS / img_width) if img_width else 0.5
        pos = self.start_landmark.normalized_coordinates()
        horizontal_axis = BodySegment(
            # start_landmark=Landmark(pos[0] - width, pos[1], 0, 1.0),
            start_landmark=Landmark(pos[0], pos[1], 0, 1.0),
            end_landmark=Landmark(pos[0] + width, pos[1], 0, 1.0)
        )
        return horizontal_axis

    def _calculate_angle(self, a: Tuple[int, int], b: Tuple[int, int])->int:
        a = np.array(a)
        b = np.array(b)
        angle_radians = np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        angle_degrees = np.degrees(angle_radians)
        """
        If arcsin is positive, the angle is between 0 and 180 degrees.
        If arcsin is negative, the angle is between 180 and 360 degrees.
        Arcsin sign is determined by the cross product of the two vectors.
        """
        cross = np.cross(a, b)
        if cross < 0:
            angle_degrees *= -1

        # if angle_degrees < 0:
        #     angle_degrees = 360 + angle_degrees
        # elif angle_degrees > 180:
        #     angle_degrees = 360 - angle_degrees
        return angle_degrees

    def vertical_axis_angle(self)->int:
        return self._calculate_angle(self.pixel_vector(), (0, 1))

    def horizontal_axis_angle(self)->int:
        return self._calculate_angle(self.pixel_vector(), (1, 0))

    def angle_between(self, other)->int:
        return self._calculate_angle(self.pixel_vector(), other.pixel_vector())

    def __str__(self):
        return f"BodySegment '{self.name}': {self.start_landmark} -> {self.end_landmark}"

    def to_dict(self):
        return {
            "start_landmark": self.start_landmark.to_dict(),
            "end_landmark": self.end_landmark.to_dict(),
            "name": self.name
        }

    def reversed(self)->'BodySegment':
        return BodySegment.reverse(self)

    @classmethod
    def reverse(cls, body_segment)->'BodySegment':
        return cls(body_segment.end_landmark, body_segment.start_landmark, name=body_segment.name)

    def draw(self, image, color:Tuple[int, int, int]=(0, 255, 0), thickness=2)->np.ndarray:
        self.start_landmark.draw(image, color, thickness=thickness)
        self.end_landmark.draw(image, color, thickness=-1)
        cv2.line(image, self.start_landmark.pixel_coordinates(image.shape[1], image.shape[0]), self.end_landmark.pixel_coordinates(image.shape[1], image.shape[0]), color, thickness)
        return image

    def _draw_angle(self, image, angle, radius=50, color:Tuple[int, int, int]=(0, 255, 0), thickness=2)->np.ndarray:
        font = cv2.FONT_HERSHEY_SIMPLEX
        pos = self.start_landmark.pixel_coordinates(image.shape[1], image.shape[0])
        cv2.putText(image, f"{int(angle)}", pos, font, 1, color, thickness, cv2.LINE_AA)
        start_angle = 0
        end_angle = angle
        rotation_angle = - self.horizontal_axis_angle()
        cv2.ellipse(image, pos, (radius, radius), rotation_angle, start_angle, end_angle, color, thickness)
                
        # Mark the start point
        start_point = get_point_on_ellipse(pos, (radius, radius), rotation_angle, start_angle)
        cv2.circle(image, start_point, 5, (255, 0, 0), -1)  # Blue circle for start point

        # Mark the end point
        end_point = get_point_on_ellipse(pos, (radius, radius), rotation_angle, end_angle)
        cv2.circle(image, end_point, 5, (0, 0, 255), -1)  # Red circle for end point

        return image

    def draw_vertical_axis_angle(self, image, radius=50, color:Tuple[int, int, int]=(0,255,0), thickness=2)->np.ndarray:
        self.vertical_body_segment(image.shape[0]).draw(image, color, thickness)
        self.draw(image, color, thickness)
        return self._draw_angle(image, self.vertical_axis_angle(), radius, color, thickness)

    def draw_horizontal_axis_angle(self, image, radius=50, color:Tuple[int, int, int]=(0,255,0), thickness=2)->np.ndarray:
        self.horizontal_body_segment(image.shape[1]).draw(image)
        self.draw(image, color, thickness)
        return self._draw_angle(image, self.horizontal_axis_angle(), radius, color, thickness)

    def draw_angle_between(self, image, other, radius=50, color:Tuple[int, int, int]=(0,255,0), thickness=2)->np.ndarray:
        other.draw(image, color, thickness)
        self.draw(image, color, thickness)
        # todo: start point should be common to both segments
        return self._draw_angle(image, self.angle_between(other), radius, color, thickness)