from enum import IntEnum
from typing import Tuple
from .body_segment import BodySegmentName

class BodyJointName(IntEnum):

    # Upper body joints
    LEFT_ELBOW = 0
    RIGHT_ELBOW = 1
    LEFT_SHOULDER = 2
    RIGHT_SHOULDER = 3
    LEFT_WRIST = 4
    RIGHT_WRIST = 5
    
    # Lower body joints
    LEFT_HIP = 6
    RIGHT_HIP = 7
    LEFT_KNEE = 8
    RIGHT_KNEE = 9
    LEFT_ANKLE = 10
    RIGHT_ANKLE = 11

    # # Torso joints
    # LEFT_SHOULDER_TO_HIP = 12
    # RIGHT_SHOULDER_TO_HIP = 13

    def __str__(self):
        return self.name

    def body_segments(self) -> Tuple[BodySegmentName, BodySegmentName]:
        """
        Define the pair of BodySegmentName instances that form this joint.
        """
        if self == BodyJointName.LEFT_ELBOW:
            return (BodySegmentName.LEFT_UPPER_ARM, BodySegmentName.LEFT_FOREARM)
        elif self == BodyJointName.RIGHT_ELBOW:
            return (BodySegmentName.RIGHT_UPPER_ARM, BodySegmentName.RIGHT_FOREARM)
        elif self == BodyJointName.LEFT_SHOULDER:
            return (BodySegmentName.LEFT_SHOULDER_TO_HIP, BodySegmentName.LEFT_UPPER_ARM)
        elif self == BodyJointName.RIGHT_SHOULDER:
            return (BodySegmentName.RIGHT_SHOULDER_TO_HIP, BodySegmentName.RIGHT_UPPER_ARM)
        elif self == BodyJointName.LEFT_WRIST:
            return (BodySegmentName.LEFT_FOREARM, BodySegmentName.LEFT_HAND)
        elif self == BodyJointName.RIGHT_WRIST:
            return (BodySegmentName.RIGHT_FOREARM, BodySegmentName.RIGHT_HAND)
        elif self == BodyJointName.LEFT_HIP:
            return (BodySegmentName.LOWER_TORSO, BodySegmentName.LEFT_THIGH)
        elif self == BodyJointName.RIGHT_HIP:
            return (BodySegmentName.LOWER_TORSO, BodySegmentName.RIGHT_THIGH)
        elif self == BodyJointName.LEFT_KNEE:
            return (BodySegmentName.LEFT_THIGH, BodySegmentName.LEFT_SHIN)
        elif self == BodyJointName.RIGHT_KNEE:
            return (BodySegmentName.RIGHT_THIGH, BodySegmentName.RIGHT_SHIN)
        elif self == BodyJointName.LEFT_ANKLE:
            return (BodySegmentName.LEFT_SHIN, BodySegmentName.LEFT_FOOT)
        elif self == BodyJointName.RIGHT_ANKLE:
            return (BodySegmentName.RIGHT_SHIN, BodySegmentName.RIGHT_FOOT)
        elif self == BodyJointName.LEFT_SHOULDER_TO_HIP:
            return (BodySegmentName.LEFT_SHOULDER_TO_HIP, BodySegmentName.LEFT_THIGH)
        elif self == BodyJointName.RIGHT_SHOULDER_TO_HIP:
            return (BodySegmentName.RIGHT_SHOULDER_TO_HIP, BodySegmentName.RIGHT_THIGH)
        else:
            raise ValueError(f"BodyJointName {self} is not supported.")
