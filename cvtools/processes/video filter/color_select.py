'''Filter colors between lower and upper bounds in BGR space'''

import cv2
import numpy as np


PARAM_DEFAULT = {
        'lower': [17, 15, 100],
        'upper': [50, 56, 200]
    }


def init(cap, param):
    lower_color_bound = np.array(param['lower'], dtype='uint8')
    upper_color_bound = np.array(param['upper'], dtype='uint8')
    background_color = (255, 255, 255)
    _, frame0 = cap.read()
    background = np.zeros(frame0.shape, np.uint8)
    background[:, :] = background_color
    init_input = {
        'background': background,
        'lower_color_bound': lower_color_bound,
        'upper_color_bound': upper_color_bound
    }
    step_input = None
    return init_input, step_input


def step(i, frame, param, init_input, step_input):
    lower_color_bound = init_input['lower_color_bound']
    upper_color_bound = init_input['upper_color_bound']
    background = init_input['background']
    mask = cv2.inRange(frame, lower_color_bound, upper_color_bound)
    f_frame = cv2.bitwise_and(frame, frame, mask=mask)
    f_frame = f_frame + cv2.add(background, f_frame, mask=cv2.bitwise_not(mask))
    filtered_frame = f_frame
    step_input = None
    return filtered_frame, step_input
