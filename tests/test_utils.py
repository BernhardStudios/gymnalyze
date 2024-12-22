import unittest
from gymnalyze.utils import load_video, draw_landmarks

class TestUtils(unittest.TestCase):

    def test_load_video(self):
        video_path = 'path/to/video.mp4'
        video = load_video(video_path)
        self.assertIsNotNone(video)

    def test_draw_landmarks(self):
        image = ...  # Load or create a test image
        landmarks = [(100, 100), (150, 150)]  # Example landmarks
        output_image = draw_landmarks(image, landmarks)
        self.assertIsNotNone(output_image)