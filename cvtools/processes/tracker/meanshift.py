from copy import copy

import cv2
import numpy as np


def init(cap, param, selection):
    _, frame = cap.read()
    c, r, w, h = selection.x, selection.y, selection.w, selection.h
    track_window = (c, r, w, h)
    roi = frame[r:r + h, c:c + w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_color_bound = param['lower_color_bound']
    upper_color_bound = param['upper_color_bound']
    color_channel = param['color_channel']
    mask = cv2.inRange(hsv_roi, np.array(lower_color_bound), np.array(upper_color_bound))
    roi_hist = cv2.calcHist([hsv_roi], color_channel, mask, [180], [0, 180])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    init_input = {'roi_hist': roi_hist, 'term_crit': term_crit, 'init_lag': 1,
                  'selection_color': selection.color}
    step_input = {'track_window': track_window, 'computed_selection': selection}
    return init_input, step_input


def step(i, frame, tracked_frame, param, init_input, step_input):
    roi_hist = init_input['roi_hist']
    term_crit = init_input['term_crit']
    init_lag = init_input['init_lag']
    selection_color = init_input['selection_color']
    computed_selection = step_input['computed_selection']
    track_window = step_input['track_window']
    color_channel = param['color_channel']
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], color_channel, roi_hist, [0, 180], 1)
    if i >= init_lag:
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)
    x, y, w, h = track_window
    tracked_frame = cv2.rectangle(tracked_frame, (x, y), (x + w, y + h), selection_color, 2)
    ncs = copy(computed_selection)
    ncs.x = x
    ncs.y = y
    ncs.w = w
    ncs.h = h
    ncs.t = i
    ncs.type = 'computed'
    step_input = {'track_window': track_window, 'computed_selection': ncs}
    return tracked_frame, step_input
