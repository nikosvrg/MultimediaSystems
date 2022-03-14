import numpy as np
import cv2


def frame_to_macroblocks(frame, k=16):
    # fit the width and height of frame so we extract same sized 16x16 macroblocks
    width = frame.shape[0]
    new_width = (width + k) - (width % k)
    height = frame.shape[1]
    new_height = (height + k) - (height % k)

    # pad the frame
    width_pad = (0, new_width - width)
    height_pad = (0, new_height - height)
    depth_pad = (0, 0)
    pad = (width_pad, height_pad, depth_pad)

    pad_frame = np.pad(frame, pad, mode='constant')

    # create 16x16 blocks
    macroblocks = []
    for i in range(0, new_width - k, k):
        row = []
        for j in range(0, new_height - k, k):
            macroblock = pad_frame[i:i + k, j:j + k]
            row.append(macroblock)
        macroblocks.append(row)

    return macroblocks


#get 2D motion vector
def get_motion_vector(macroblock, reference_frame, coords, macroblock_size):
    k = macroblock_size
    #discrete neighbor plane of frames
    neighbors = [0, k / 2, -k / 2]
    #sad metric for first and next frame
    best = get_sad(macroblock, reference_frame[coords[0]:coords[0] + macroblock_size, coords[1]:coords[1] + macroblock_size])
    best_coords = coords
    while True:
        for i in range(len(neighbors)):
            for j in range(len(neighbors)):
                if neighbors[i] == neighbors[j] == 0:
                    continue
            try:
                #look to find next best position of  macroblocks for transition
                temp = get_sad(macroblock,
                           reference_frame[int(best_coords[0] + neighbors[i]):int(best_coords[0] + macroblock_size + neighbors[i]),
                               int(best_coords[1] + neighbors[j]):int(best_coords[1] + macroblock_size + neighbors[j])])
                if temp < best:
                    best = temp
                    best_coords = (best_coords[0] + neighbors[i], best_coords[1] + neighbors[j])
            except IndexError:
                pass
	    #at step 1=probably best break
        neighbors[:] = [step / 2 for step in neighbors]
        if neighbors[1] < 1:
            break

    return tuple(np.subtract(best_coords, coords, dtype=int, casting='unsafe'))




#get sum of absolute diffrence
def get_sad(previous_macroblock,next_macroblock):
    value = 0
    n = previous_macroblock.shape[0]
    for i in range(n):
        for j in range(n):
            previous_pixel = int(previous_macroblock[i, j])
            next_pixel = int(next_macroblock[i, j])
            value += abs(next_pixel - previous_pixel)

    return value


#sad for color values
#could implement on metric vector later on
def get_sad_color(previous_macroblock,next_macroblock):
        cvalue = 0
        n = previous_mb.shape[0]
        for i in range(n):
            for j in range(n):
                previous_pixel =  previous_macroblock[i,j]
                next_pixel = next_macroblock[i,j]

                for c in range(3):
                    previous_color = int(previous_pixel[c])
                    next_color = int(next_pixel[c])
                    cvalue = abs(next_color - previous_color)
        return cvalue	


#get best match and extract each macroblock
#same algorithmic thought of get_motion_vector
def get_best_match(previous_motion, next_row, next_col, next_motion, k=16):
    step = k / 2
    result = None

    while step != 1:
        # find closest index neighbors
        neighbors = []

        try:
            neighbors.append([next_row + 1, next_col + 1, previous_motion[next_row + 1][next_col + 1]])
        except IndexError:
            pass

        try:
            neighbors.append([next_row - 1, next_col - 1, previous_motion[next_row - 1][next_col - 1]])
        except IndexError:
            pass

        try:
            neighbors.append([next_row + 1, next_col - 1, previous_motion[next_row + 1][next_col - 1]])
        except IndexError:
            pass

        try:
            neighbors.append([next_row - 1, next_col + 1, previous_motion[next_row - 1][next_col + 1]])
        except IndexError:
            pass

        try:
            neighbors.append([next_row + 1, next_col, previous_motion[next_row + 1][next_col]])
        except IndexError:
            pass

        try:
            neighbors.append([next_row, next_col - 1, previous_motion[next_row][next_col - 1]])
        except IndexError:
            pass

        try:
            neighbors.append([next_row, next_col + 1, previous_motion[next_row][next_col + 1]])
        except IndexError:
            pass

        try:
            neighbors.append([next_row - 1, next_col, previous_motion[next_row - 1][next_col]])
        except IndexError:
            pass

        sad_values = [get_sad_color(neighbor[2], next_motion) for neighbor in neighbors]
        min_sad = min(sad_values)

        min_index = sad_values.index(min_sad)
        next_row, next_col, next_motion = neighbors[min_index]

        step /= 2
        result = next_motion

    return result

