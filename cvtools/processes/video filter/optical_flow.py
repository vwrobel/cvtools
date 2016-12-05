import cv2
import numpy as np

PARAM_DEFAULT = {
    'pyr_scale': 0.5,
    'levels': 3,
    'win_size': 15,
    'iterations': 3,
    'poly_n': 5,
    'poly_sigma': 1.1
}


def init(cap, param):
    if not param:
        param = PARAM_DEFAULT
    iterations = param['iterations']
    levels = param['levels']
    pyr_scale = param['pyr_scale']
    win_size = param['win_size']
    poly_n = param['poly_n']
    poly_sigma = param['poly_sigma']
    _, frame0 = cap.read()
    prvs = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    ret, frame1 = cap.read()
    next = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, pyr_scale, levels, win_size,
                                        iterations, poly_n, poly_sigma, 0)
    prvs = next
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255
    init_input = {
        'init_lag': 2
    }
    step_input = {
        'prvs': prvs,
        'flow': flow,
        'hsv': hsv
    }
    return init_input, step_input


def step(i, frame, param, init_input, step_input):
    iterations = param['iterations']
    levels = param['levels']
    pyr_scale = param['pyr_scale']
    win_size = param['win_size']
    poly_n = param['poly_n']
    poly_sigma = param['poly_sigma']
    init_lag = init_input['init_lag']
    prvs = step_input['prvs']
    flow = step_input['flow']
    hsv = step_input['hsv']

    if i >= init_lag:
        next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.calcOpticalFlowFarneback(prvs, next, flow, pyr_scale, levels, win_size,
                                     iterations, poly_n, poly_sigma, cv2.OPTFLOW_USE_INITIAL_FLOW)
        prvs = next
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        filtered_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        step_input = {
            'prvs': prvs,
            'flow': flow,
            'hsv': hsv
        }
    else:
        filtered_frame = np.zeros(frame.shape, np.uint8)
    return filtered_frame, step_input
