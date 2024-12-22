import unittest
from gymnalyze.pose_estimator import PoseEstimator

class TestPoseEstimator(unittest.TestCase):

    def setUp(self):
        self.pose_estimator = PoseEstimator()

    def test_estimate_pose(self):
        # Test with a sample frame (replace with actual frame data)
        frame = None  # Placeholder for an actual video frame
        pose = self.pose_estimator.estimate_pose(frame)
        self.assertIsNotNone(pose)

    def test_get_landmarks(self):
        # Test with a sample pose (replace with actual pose data)
        pose = None  # Placeholder for an actual pose data
        landmarks = self.pose_estimator.get_landmarks(pose)
        self.assertIsNotNone(landmarks)
        self.assertIsInstance(landmarks, list)

if __name__ == '__main__':
    unittest.main()