import numpy as np
from typing import Tuple, Optional
from .body_segment import BodySegment

class BodyJoint:

    def __init__(self, start_body_segment: BodySegment, end_body_segment: BodySegment, name: Optional[str] = None):
        self.start_body_segment = start_body_segment
        self.end_body_segment = end_body_segment
        self.name = name

        # check both body segments have the same image shape
        if self.start_body_segment.width != self.end_body_segment.width or self.start_body_segment.height != self.end_body_segment.height:
            raise ValueError(f"[{self.name}] Both body segments should have the same image shape")
        else:
            self.width = self.start_body_segment.width
            self.height = self.start_body_segment.height

        # Create a set of common landmarks
        common_landmarks = set(self.start_body_segment.landmarks()).intersection(set(self.end_body_segment.landmarks()))
        if len(common_landmarks) != 1:
            raise ValueError(f"[{self.name}] Both body segments should have exactly one common landmark")
        else:
            self.common_landmark = common_landmarks.pop()
            
        # Check both body segments start with the common landmark
        if self.start_body_segment.start_landmark != self.common_landmark:
            self.start_body_segment = self.start_body_segment.reversed()

        if self.end_body_segment.start_landmark != self.common_landmark:
            self.end_body_segment = self.end_body_segment.reversed()


    def angle(self)->int:
        return self.start_body_segment.angle(self.end_body_segment)

    def draw(self, image, color:Tuple[int, int, int]=(0, 255, 0), radius=50, thickness=2)->np.ndarray:
        return self.start_body_segment.draw_angle_between(image, self.end_body_segment, radius, color, thickness)

    def __str__(self):      
        return f"BodyJoint '{self.name}': angle={self.angle()}"

    def to_dict(self):
        return {
            "start_body_segment": self.start_body_segment.to_dict(),
            "end_body_segment": self.end_body_segment.to_dict(),
            "name": self.name
        }