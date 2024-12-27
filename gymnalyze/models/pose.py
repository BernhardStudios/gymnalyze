from typing import List, Dict
from .landmark import Landmark
from .body_segment import BodySegment
from ..enums.landmark import LandmarkName
from ..enums.body_segment import BodySegmentName

class Pose:
    def __init__(self, landmarks: List[Dict]):

        landmarks = [ {
            "x": l.x, "y": l.y, "z": l.z, "visibility": l.visibility
        } for l in landmarks ]

        # Add virtual landmarks: MID_SHOULDER
        landmarks.append(
            Landmark(
                x=(landmarks[LandmarkName.LEFT_SHOULDER].get("x") + landmarks[LandmarkName.RIGHT_SHOULDER].get("x")) / 2,
                y=(landmarks[LandmarkName.LEFT_SHOULDER].get("y") + landmarks[LandmarkName.RIGHT_SHOULDER].get("y")) / 2,
                z=(landmarks[LandmarkName.LEFT_SHOULDER].get("z") + landmarks[LandmarkName.RIGHT_SHOULDER].get("z")) / 2,
                visibility=(landmarks[LandmarkName.LEFT_SHOULDER].get("visibility") + landmarks[LandmarkName.RIGHT_SHOULDER].get("visibility")) / 2,
            ).to_dict(), 
        )
        # Add virtual landmarks: MID_HIP
        landmarks.append(
            Landmark(
                x=(landmarks[LandmarkName.LEFT_HIP].get("x") + landmarks[LandmarkName.RIGHT_HIP].get("x")) / 2,
                y=(landmarks[LandmarkName.LEFT_HIP].get("y") + landmarks[LandmarkName.RIGHT_HIP].get("y")) / 2,
                z=(landmarks[LandmarkName.LEFT_HIP].get("z") + landmarks[LandmarkName.RIGHT_HIP].get("z")) / 2,
                visibility=(landmarks[LandmarkName.LEFT_HIP].get("visibility") + landmarks[LandmarkName.RIGHT_HIP].get("visibility")) / 2,
            ).to_dict()
        )

        self.landmarks = {
            LandmarkName(i) : Landmark(lm.get("x"), lm.get("y"), lm.get("z"), lm.get("visibility"), name=LandmarkName(i).name) for i,lm in enumerate(landmarks)
        }
        self.body_segments = {
            segment : BodySegment(self.landmarks[segment.landmarks()[0]], self.landmarks[segment.landmarks()[1]], name=segment.name) 
            for segment in BodySegmentName
        }

    def __str__(self):
        return f"PoseData with {len(self.landmarks)} landmarks"