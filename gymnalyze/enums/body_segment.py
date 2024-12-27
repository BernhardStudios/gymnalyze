from enum import IntEnum
from typing import Tuple
from .landmark import LandmarkName


class BodySegmentName(IntEnum):

    # upper limbs
    LEFT_UPPER_ARM = 0
    RIGHT_UPPER_ARM = 1
    LEFT_FOREARM = 2
    RIGHT_FOREARM = 3
    # lower limbs
    LEFT_THIGH = 4
    RIGHT_THIGH = 5
    LEFT_SHIN = 6
    RIGHT_SHIN = 7
    # torso
    UPPER_TORSO = 8
    LOWER_TORSO = 9
    SPINE = 10
    # other derived body parts
    LEFT_SHOULDER_TO_HIP = 11
    RIGHT_SHOULDER_TO_HIP = 12

    def __str__(self):
        return self.name

    def landmarks(self)->Tuple[LandmarkName, LandmarkName]:
        if self == BodySegmentName.LEFT_UPPER_ARM:
            return [LandmarkName.LEFT_SHOULDER, LandmarkName.LEFT_ELBOW]
        elif self == BodySegmentName.RIGHT_UPPER_ARM:
            return [LandmarkName.RIGHT_SHOULDER, LandmarkName.RIGHT_ELBOW]
        elif self == BodySegmentName.LEFT_FOREARM:
            return [LandmarkName.LEFT_ELBOW, LandmarkName.LEFT_WRIST]
        elif self == BodySegmentName.RIGHT_FOREARM:
            return [LandmarkName.RIGHT_ELBOW, LandmarkName.RIGHT_WRIST]
        elif self == BodySegmentName.LEFT_THIGH:
            return [LandmarkName.LEFT_HIP, LandmarkName.LEFT_KNEE]
        elif self == BodySegmentName.RIGHT_THIGH:
            return [LandmarkName.RIGHT_HIP, LandmarkName.RIGHT_KNEE]
        elif self == BodySegmentName.LEFT_SHIN:
            return [LandmarkName.LEFT_KNEE, LandmarkName.LEFT_ANKLE]
        elif self == BodySegmentName.RIGHT_SHIN:
            return [LandmarkName.RIGHT_KNEE, LandmarkName.RIGHT_ANKLE]
        elif self == BodySegmentName.UPPER_TORSO:
            return [LandmarkName.LEFT_SHOULDER, LandmarkName.RIGHT_SHOULDER]
        elif self == BodySegmentName.LOWER_TORSO:
            return [LandmarkName.LEFT_HIP, LandmarkName.RIGHT_HIP]
        elif self == BodySegmentName.SPINE:
            return [LandmarkName.MID_SHOULDER, LandmarkName.MID_HIP]   
        elif self == BodySegmentName.LEFT_SHOULDER_TO_HIP:
            return [LandmarkName.LEFT_SHOULDER, LandmarkName.LEFT_HIP]
        elif self == BodySegmentName.RIGHT_SHOULDER_TO_HIP:
            return [LandmarkName.RIGHT_SHOULDER, LandmarkName.RIGHT_HIP]
        else:
            raise ValueError(f"BodySegmentName {self} not supported")