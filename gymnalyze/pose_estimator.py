class PoseEstimator:
    def __init__(self):
        import mediapipe as mp
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

    def estimate_pose(self, frame):
        results = self.pose.process(frame)
        return results

    def get_landmarks(self, pose):
        if pose.pose_landmarks:
            return [(landmark.x, landmark.y, landmark.z) for landmark in pose.pose_landmarks.landmark]
        return []