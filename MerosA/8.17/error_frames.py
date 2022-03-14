import cv2

# Load the video to process each frame.
video = cv2.VideoCapture('../Meros A/8.17/videos/ball.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('g8-17a.avi', fourcc, video.get(5),
                         (int(video.get(3)), int(video.get(4))), False)

previous_frame = None

while video.isOpened():
    success, current_frame = video.read()

    # Break if the video has ended.
    if not success:
        break

    # Keep the previous frame except on first iteration.
    if previous_frame is None:
        previous_frame = current_frame.copy()
        continue

    # difference between the current and the previous frame.
    error_frame_img = cv2.absdiff(current_frame, previous_frame)
    grey = cv2.cvtColor(error_frame_img, cv2.COLOR_BGR2GRAY)
    #hsv = cv2.cvtColor(error_frame_img, cv2.COLOR_BGR2HSV)
    cv2.imshow('Error Frames', error_frame_img)
    output.write(error_frame_img)
    cv2.waitKey(60)

    # Keep the previous frame.
    prev_frame = current_frame.copy()

video.release()
cv2.destroyAllWindows()