import numpy as np
import cv2
import time

from functions import get_motion_vector

macroblock_size = 16


video = cv2.VideoCapture('../Meros A/8.17/videos/video1.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('motion8.17b.avi', fourcc, video.get(5),(int(video.get(3)), int(video.get(4))), False)
start = time.time()
frames = 1

#fix frame size of reference and current frame
def fix_frame_shape(frame):
    return np.pad(frame, ((0, int((np.ceil(video.get(4) / macroblock_size) * macroblock_size) - video.get(4))),
                          (0, int((np.ceil(video.get(3) / macroblock_size) * macroblock_size) - video.get(3)))),
                  'constant', constant_values=0)


ref, reference_frame = video.read()
reference_frame = fix_frame_shape(cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY))
print("Frame #1 of "  + " Completed.") #information message.
while video.isOpened():
    ref, current_frame = video.read()
    if not ref:
        break
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    current_frame = fix_frame_shape(current_frame)
    temp = np.zeros((reference_frame.shape[0], reference_frame.shape[1]), dtype = np.uint8)
    for i in range(0, current_frame.shape[0], macroblock_size):
        for j in range(0, current_frame.shape[1], macroblock_size):
            motion_vector = get_motion_vector(current_frame[i:i+macroblock_size,j:j+macroblock_size], reference_frame, (i,j))
            cv2.subtract(current_frame[i:i + macroblock_size, j:j + macroblock_size],
                         reference_frame[i + motion_vector[0]:i + macroblock_size + motion_vector[0],
                         j+ motion_vector[1]:j + macroblock_size + motion_vector[1]],
                         temp[i:i+macroblock_size, j:j+macroblock_size])
    reference_frame = current_frame
    temp = np.delete(temp , slice(int(video.get(4)),None),0)
    templ = np.delete(temp, slice(int(video.get(3)),None),1)
    output.write(temp)
    frames += 1
    print('Frames Processed: ' + str(frames))

video.release()
output.release()
print('Time elapsed: ' + str(round(time.time() - start)) + 's')


