import cv2
import numpy as np

from functions import frame_to_macroblocks, get_best_match


#get best match and extract macroblocks

video = cv2.VideoCapture('../Meros A/8.17/videos/ball.mp4')


_, previous_frame = video.read()
_, next_frame = video.read()

frames = np.concatenate((previous_frame, next_frame), axis=0)
cv2.imshow('First and second frame', frames)


# Extract all macroblocks from the two loaded frames.
previous_macroblock = frame_to_macroblocks(previous_frame)
next_macroblock = frame_to_macroblocks(next_frame)

# Loop through each macroblock on the second frame.
for row, macroblocks in enumerate(next_macroblock):
    for col, macroblock in enumerate(macroblocks):
        # Find the best matching macroblock from the previous frame.
        match = get_best_match(previous_macroblock, row, col, macroblock)

        # Show best match, current macroblock and difference.
        diff = cv2.absdiff(macroblock, match)
        #macroblock extraction first image
        pad = cv2.copyMakeBorder(macroblock, 0, 0, 0, 5, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        #macroblock extraction of matched image
        match_pad = cv2.copyMakeBorder(macroblock, 0, 0, 0, 5, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        image = np.concatenate((pad, match_pad, diff), axis=1)


        cv2.imshow('Macroblock best match ', image)

        cv2.waitKey(10)

video.release()
cv2.destroyAllWindows()