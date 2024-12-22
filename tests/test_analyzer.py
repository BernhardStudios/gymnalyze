import unittest
from gymnalyze.analyzer import PoseAnalyzer

class TestPoseAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = PoseAnalyzer()

    def test_analyze_video(self):
        video_path = "path/to/test/video.mp4"
        result = self.analyzer.analyze_video(video_path)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)  # Assuming the result is a dictionary

    def test_assess_pose(self):
        pose_data = {"keypoints": [0.5, 0.5], "score": 0.9}
        assessment = self.analyzer.assess_pose(pose_data)
        self.assertIsNotNone(assessment)
        self.assertIn("assessment", assessment)  # Assuming the assessment contains a key "assessment"

if __name__ == '__main__':
    unittest.main()