import cv2
import json
import mediapipe as mp
import numpy as np
from gymnalyze.models.pose import Pose
from gymnalyze.utils import Color
from gymnalyze.enums import BodySegmentName
from gymnalyze.enums import LandmarkName, BodySegmentName, BodyJointName

def main():

    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Video path
    video_path = '.demo_data/kipping-pull-up-complete.mp4'

    # Load video using opencv
    cap = cv2.VideoCapture(video_path)
    
    # Check if video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # Print key event instructions
    print("Instructions:")
    print("> Press 'q' to quit.")
    print("> Press ' ' (spacebar) to pause/play.")
    print("> Press 'r' to rewind 30 frames.")
    print("> Press 'f' to fast forward 30 frames.")
    print("> Press '+' to increase speed.")
    print("> Press '-' to decrease speed.")

    playing = True
    frame_pos = 0

    DEFAULT_DELAY = 25 * 3 # Initial delay in milliseconds
    delay = DEFAULT_DELAY  

    while cap.isOpened():
        if playing:
            ret, frame = cap.read()
            if not ret:
                break

            frame_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform pose detection
            results = pose.process(frame_rgb)

            my_pose = Pose(results, img_shape=frame_rgb.shape)

            # Define a white canvas with same dimensions as the frame
            canvas = np.ones_like(frame) * 255

            # # Draw body segments
            # for segment in BodySegmentName:
            #     my_pose.body_segments[segment].draw(canvas, color=Color.RED, thickness=2)
            #     # draw vertical axis angle
            #     my_pose.body_segments[segment].draw_vertical_axis_angle(canvas, radius=50, color=Color.BLUE, thickness=2)

            for joint in BodyJointName:
                # if joint != 0:
                #     continue
                my_pose.body_joints[joint].draw(canvas, color=Color.GREEN, radius=50)

            # Blend the canvas with the frame
            # Define transparency as 0.5
            transparency = 0.25
            frame = cv2.addWeighted(frame, transparency, canvas, 1-transparency, 0)

            # put frame number as text in the top left corner
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (10, 30)  # Top left corner
            frame = cv2.putText(frame, f"Frame: {frame_pos}", org, font, 1, Color.BLACK, 2, cv2.LINE_AA)

            # Display the resulting frame
            cv2.imshow('Demo', frame)

        # Handle key events
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('q'):
            print("Key 'q' pressed. Exiting.")
            break
        elif key == ord(' '):  # Spacebar to pause/play
            playing = not playing
            print("Spacebar pressed. Playing:", playing)
            # reset delay to 25ms
            delay = DEFAULT_DELAY
        elif key == ord('r'):  # 'r' to rewind
            frame_pos = max(frame_pos - 30, 0)  # Rewind by 30 frames
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            print("'r' pressed. Rewinding to frame:", frame_pos)
        elif key == ord('f'):  # 'f' to fast forward
            frame_pos = min(frame_pos + 30, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            print("'f' pressed. Fast forwarding to frame:", frame_pos)
        elif key == ord('+'):  # '+' to increase speed
            delay = max(1, delay - 5)  # Decrease delay to increase speed
            print("'+' pressed. Increasing speed. Delay:", delay)
        elif key == ord('-'):  # '-' to decrease speed
            delay += 5  # Increase delay to decrease speed
            print("'-' pressed. Decreasing speed. Delay:", delay)
        elif key == ord('s'): # save pose from current frame as dict
            data = my_pose.to_dict()
            with open(f'pose_data_frame_{frame_pos}.json', 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Pose data saved to pose_data_frame_{frame_pos}.json")
            image_path = f'frame_{frame_pos}.png'
            cv2.imwrite(image_path, frame)
            print(f"Frame saved as {image_path}")

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()