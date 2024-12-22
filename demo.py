import cv2

def main():

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

    DEFAULT_DELAY = 25 # Initial delay in milliseconds
    delay = DEFAULT_DELAY  

    while cap.isOpened():
        if playing:
            ret, frame = cap.read()
            if not ret:
                break

            frame_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

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

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()