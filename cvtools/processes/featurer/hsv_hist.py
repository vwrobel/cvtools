import cv2
import numpy as np


def hsv_hist(roi,
             lower_color_bound,
             upper_color_bound,
             color_channel,
             bin_nb,
             channel_range):
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array(lower_color_bound), np.array(upper_color_bound))
    roi_hist = cv2.calcHist([hsv_roi], color_channel, mask, bin_nb, channel_range)
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    return roi_hist
