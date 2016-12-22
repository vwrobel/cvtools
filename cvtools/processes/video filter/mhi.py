import cv2
import numpy as np
from skimage import img_as_ubyte
import warnings

PARAM_DEFAULT = {
    'sigma_blur': 9,
    'threshold': 5,
    'kernel_size': 5,
    'tau': 200
}


def init(cap, param):
    sigma_blur = param['sigma_blur']
    _, frame0 = cap.read()
    gray = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY) * 1.0
    gray_blur = cv2.GaussianBlur(gray, (sigma_blur, sigma_blur), 0)
    mhi = np.zeros(gray.shape)
    init_input = {
        'init_lag': 1
    }
    step_input = {
        'mhi': mhi,
        'gray_blur': gray_blur
    }
    return init_input, step_input


def step(i, frame, param, init_input, step_input):
    sigma_blur = param['sigma_blur']
    threshold = param['threshold']
    kernel_size = param['kernel_size']
    tau = param['tau']
    mhi = step_input['mhi']
    init_lag = init_input['init_lag']
    gray_blur_old = step_input['gray_blur']
    if i >= init_lag:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) * 1.0
        gray_blur = cv2.GaussianBlur(gray, (sigma_blur, sigma_blur), 0)
        diff = gray_blur - gray_blur_old

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        B = cv2.morphologyEx((np.abs(diff) > threshold) * 1.0, cv2.MORPH_OPEN, kernel)
        mhi[B == 0] = np.maximum(0, mhi[B == 0] - 1)
        mhi[B > 0] = tau

        f_frame = mhi / tau
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            f_frame = img_as_ubyte(f_frame)
        f_frame = cv2.cvtColor(f_frame, cv2.COLOR_GRAY2BGR)
        filtered_frame = f_frame
        step_input = {
            'mhi': mhi,
            'gray_blur': gray_blur
        }
    else:
        filtered_frame = np.zeros(frame.shape, np.uint8)
    return filtered_frame, step_input
