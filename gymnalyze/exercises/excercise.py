from typing import Tuple, List, Optional
import numpy as np
import cv2

from ..utils import MonotonicAnalyzer, Color
from ..models.pose import Pose
from ..enums import LandmarkName, BodySegmentName, BodyJointName

class Exercise:

    LANDMARKS_OF_INTEREST = [
    ]

    BODY_SEGMENTS_OF_INTEREST = [
    ]

    BODY_JOINTS_OF_INTEREST = [
    ]

    def __init__(self, k: int = 2, smoothing_factor: int = 1000, frame_evaluation_interval: int = 6):

        self.k = k
        self.smoothing_factor = smoothing_factor
        self.analyzer = None # it will be updated later
        self.frame_pos = None

        self.frame_evaluation_interval = frame_evaluation_interval

        self.pose_data = {
            'landmarks'     : { ln : {} for ln in self.LANDMARKS_OF_INTEREST     },
            'body_segments' : { bs : {} for bs in self.BODY_SEGMENTS_OF_INTEREST },
            'body_joints'   : { bj : {} for bj in self.BODY_JOINTS_OF_INTEREST   },
        }

    def append_pose(self, frame_pos: int, pose: Pose):

        self.frame_pos = frame_pos
        
        for landmark in self.LANDMARKS_OF_INTEREST:
            self.pose_data['landmarks'][landmark].update({frame_pos: pose.landmarks[landmark]})

        for segment in self.BODY_SEGMENTS_OF_INTEREST:
            self.pose_data['body_segments'][segment].update({frame_pos: pose.body_segments[segment]})

        for joint in self.BODY_JOINTS_OF_INTEREST:
            self.pose_data['body_joints'][joint].update({frame_pos: pose.body_joints[joint]})
        
        if frame_pos % self.frame_evaluation_interval == 0:
            self.analyzer = self.update_monotonic_analizer()

    def update_monotonic_analizer(self)->MonotonicAnalyzer:
        # todo: in a future allow values to be a list o lists, and combine them in MonotonicAnalyzer (convolution)
        frame_idx, values = self._transform_pose_to_monotonic_analyzer_input()[0]
        return MonotonicAnalyzer(frame_idx, values, self.k, self.smoothing_factor)

    def _transform_pose_to_monotonic_analyzer_input(self)->List[Tuple[List[int], List[float]]]:
        # ! This has to be updated for each exercise
        raise ValueError("Please implement this method in the child class")

    @property
    def n_reps(self)->int:
        # todo: implement this
        pass

    @property
    def n_valid_reps(self)->int:
        # todo: implement this
        pass

    @property
    def is_valid_rep(self)->bool:
        # todo: implement this
        pass

    def draw(self, img: np.ndarray, frame_pos: Optional[int]=None, color: Tuple[int, int, int] = Color.TEAL)->np.ndarray:
        if not frame_pos:
            frame_pos = self.frame_pos
        for landmark in self.LANDMARKS_OF_INTEREST:
            self.pose_data['landmarks'][landmark][frame_pos].draw(img, color)
        for segment in self.BODY_SEGMENTS_OF_INTEREST:
            self.pose_data['body_segments'][segment][frame_pos].draw(img, color)
        for joint in self.BODY_JOINTS_OF_INTEREST:
            self.pose_data['body_joints'][joint][frame_pos].draw(img, color)
        return img

    def bind_monotonic_analyzer_to_frame(self, frame: np.ndarray)->np.ndarray:

        img_1 = frame.copy()

        BASE_FRAME_SIZE = (20, 15)
        frame_size = BASE_FRAME_SIZE[0], int(BASE_FRAME_SIZE[0] * frame.shape[0] / frame.shape[1])

        if self.analyzer:
            img_2 = cv2.resize(self.analyzer.plot_img, img_1.shape[:2][::-1])
        else:
            img_2 = np.ones_like(img_1) * 255

        return cv2.hconcat([img_1, img_2])