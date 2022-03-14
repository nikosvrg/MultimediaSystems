import numpy as np
import cv2
import time

from functions import get_sad, get_motion_vector

#change to 8,4
macroblock_size = 16


video = cv2.VideoCapture('../Meros A/8.18/videos/fallingball.mp4')

start = time.time()
frames = 1

#
def fix_frame_shape(frame):
    return np.pad(frame, ((0, int((np.ceil(video.get(4) / macroblock_size) * macroblock_size) - video.get(4))),
                          (0, int((np.ceil(video.get(3) / macroblock_size) * macroblock_size) - video.get(3)))),
                  'constant', constant_values=0)




total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
reference_frame, background_frame = video.read()
background_frame = cv2.cvtColor(background_frame, cv2.COLOR_BGR2GRAY)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter(str(macroblock_size) + 'mb_objectremoved.avi', fourcc, video.get(5),
                         (int(video.get(3)), int(video.get(4))), False)

background_frame = fix_frame_shape(background_frame)
output.write(background_frame)


ref_frame = background_frame

print("Frame #" + str(frames) + " of " + str(total_frames) + " Completed")

while video.isOpened():
    reference_frame, current_frame = video.read()
    if not reference_frame:
        break
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    current_frame = fix_frame_shape(current_frame)
    for i in range(0, current_frame.shape[0], macroblock_size):
        for j in range(0, current_frame.shape[1], macroblock_size):
            motion_v = get_motion_vector(current_frame[i:i + macroblock_size, j:j + macroblock_size], rbg_frame, (i, j), macroblock_size)
            if motion_v[0] + motion_v[1] != 0:
                current_frame[i:i + macroblock_size, j:j + macroblock_size] = background_frame[i:i + macroblock_size,
                                                                             j:j + macroblock_size]
    reference_frame = current_frame
    current_frame = np.delete(current_frame, slice(int(video.get(4)), None), 0)
    current_frame = np.delete(current_frame, slice(int(video.get(3)), None), 1)
    output.write(current_frame)
    frames += 1
    print("Frame #" + str(frames) + " of " + str(total_frames) + " Completed")

video.release()
output.release()
print('Time elapsed: ' + str(round(time.time() - start)) + 's')
