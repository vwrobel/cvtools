import cv2
import numpy as np
from copy import copy
from ..featurer.hsv_hist import hsv_hist

PARAM_DEFAULT = {
    'lower_color_bound': [0.0, 0.0, 0.0],
    'upper_color_bound': [255.0, 255.0, 255.0],
    'color_channel': [2],
    'channel_range': [0, 180],
    'bin_nb': [16]
}


def init(cap, param, selection):
    lower_color_bound = param['lower_color_bound']
    upper_color_bound = param['upper_color_bound']
    color_channel = param['color_channel']
    channel_range = param['channel_range']
    bin_nb = param['bin_nb']

    t = selection.t
    cap.set(cv2.CAP_PROP_POS_FRAMES, t)
    _, frame = cap.read()

    track_window = selection.get_window()
    roi = selection.get_roi(frame)

    roi_hist = hsv_hist(roi, lower_color_bound, upper_color_bound,
                        color_channel, bin_nb, channel_range)
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    init_input = {'roi_hist': roi_hist, 'term_crit': term_crit, 'init_lag': 1,
                  'start_track': t, 'selection_color': selection.color, 'selection_name': selection.name}
    step_input = {'track_window': track_window, 'computed_selection': selection, 'track_started': False}
    return init_input, step_input


def step(i, frame, tracked_frame, param, init_input, step_input):
    roi_hist = init_input['roi_hist']
    term_crit = init_input['term_crit']
    init_lag = init_input['init_lag']
    start_track = init_input['start_track']
    selection_color = init_input['selection_color']
    selection_name = init_input['selection_name']
    computed_selection = step_input['computed_selection']
    track_window = step_input['track_window']
    color_channel = param['color_channel']
    channel_range = param['channel_range']
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], color_channel, roi_hist, channel_range, 1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if i >= start_track + init_lag:
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)
        x, y, w, h = track_window
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        tracked_frame = cv2.polylines(frame, [pts], True, selection_color, 2)
        tracked_frame = cv2.putText(tracked_frame, selection_name, (x, y - 20), font, 1, selection_color)
    else:
        x, y, w, h = track_window
        tracked_frame = cv2.rectangle(tracked_frame, (x, y), (x + w, y + h), selection_color, 2)
        tracked_frame = cv2.putText(tracked_frame, selection_name, (x, y - 20), font, 1, selection_color)
    ncs = copy(computed_selection)
    ncs.x = x
    ncs.y = y
    ncs.w = w
    ncs.h = h
    ncs.t = i
    ncs.type = 'computed'
    step_input = {'track_window': track_window, 'computed_selection': ncs, 'track_started': True}
    return tracked_frame, step_input

