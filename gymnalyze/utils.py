def load_video(video_path):
    import cv2
    video = cv2.VideoCapture(video_path)
    return video

def draw_landmarks(image, landmarks):
    import cv2
    for landmark in landmarks:
        x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
    return image